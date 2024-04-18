
from fastapi import APIRouter, Request, Depends, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from loguru import logger
import uuid
import json
from redis.asyncio import Redis

from scenes.scenes import SCENES, DEFAULT_SCENE, ERROR_SCENE
from services.tts import get_tts, Speech_and_text
from services.text_handling.extractor import (
    get_extractor, EntityExtractor)
from services.request_parsers import RequestParser, get_request_parser_duke
from db.redis import get_redis


router = APIRouter()


@router.post("/alice")
async def alice(request: Request):

    event = await request.json()
    curent_intent = event.get('request', {}).get('nlu', {}).get('intents', {})
    new_session = event.get('session', {}).get('new')
    logger.debug('curent_intent is', curent_intent)

    if new_session:
        return await DEFAULT_SCENE().reply(request)
    try:
        label = next(iter(curent_intent))
    except StopIteration:
        return await ERROR_SCENE().reply(request)

    current_scene = SCENES.get(label, DEFAULT_SCENE)()

    request_parser = RequestParser(event)
    next_scene = await current_scene.move(request_parser)

    if next_scene is not None:
        logger.info(f'Moving from scene {current_scene.id()} to {next_scene.id()}')
        return await next_scene.reply(request)
    else:
        logger.info(f'Failed to parse user request at scene {current_scene.id()}')
        return await current_scene.fallback(request)


@router.post("/duke")
async def duke(req: Request,
               file_input: UploadFile = File(...),
               tts: Speech_and_text = Depends(get_tts),
               extractor: EntityExtractor = Depends(get_extractor),
               redis: Redis = Depends(get_redis)):

    transcription = await tts.recognize(file_input)

    curent_intent = await extractor.process_text_async(transcription)
    logger.debug('curent_intent is', curent_intent)

    session = req.session
    session_id = session.get('session_id')

    if not session_id:
        session["session_id"] = str(uuid.uuid4())
        session_id = session.get('session_id')

    curent_intent['session_id'] = session_id

    request_parser = await get_request_parser_duke(curent_intent)

    if not curent_intent:
        return await DEFAULT_SCENE().reply(request_parser)

    label = curent_intent['label']
    current_scene = SCENES.get(label, DEFAULT_SCENE)()

    next_scene = await current_scene.move(request_parser)

    if next_scene is not None:
        logger.info(
            f'Moving from scene {current_scene.id()} to {next_scene.id()}')
        logger.info(curent_intent)
        reply = await next_scene.reply(request_parser)
        searched_ents = reply.get('session_state')
        await redis.setex(
            session["session_id"], 3600, json.dumps(searched_ents))
        reply_tts = reply.get('response', {}).get('tts')

        aud = await tts.dictate(reply_tts)
        return FileResponse(aud, media_type='audio/mpeg', filename='audio.mp3')
    else:
        logger.error(
            f'Failed to parse user request {transcription} at scene {current_scene.id()}')
        return await current_scene.fallback(request_parser)


class TextInput(BaseModel):
    text: str


@router.post("/duke_textual")
async def duke_textual(text_input: TextInput,
                       req: Request,
                       extractor: EntityExtractor = Depends(get_extractor),
                       redis: Redis = Depends(get_redis)):

    curent_intent = await extractor.process_text_async(text_input.text)
    logger.debug('curent_intent is', curent_intent)
    session = req.session
    session_id = session.get('session_id')

    if not session_id:
        session["session_id"] = str(uuid.uuid4())
        session_id = session.get('session_id')

    curent_intent['session_id'] = session_id

    request_parser = await get_request_parser_duke(curent_intent)

    if not curent_intent:
        return await DEFAULT_SCENE().reply(request_parser)

    label = curent_intent['label']
    current_scene = SCENES.get(label, DEFAULT_SCENE)()

    next_scene = await current_scene.move(request_parser)

    if next_scene is not None:
        logger.info(
            f'Moving from scene {current_scene.id()} to {next_scene.id()}')
        reply = await next_scene.reply(request_parser)
        searched_ents = reply.get('session_state')
        await redis.setex(
            session["session_id"], 3600, json.dumps(searched_ents))
        return reply
    else:
        logger.error(
            f'Failed to parse user request {text_input.text} at scene {current_scene.id()}')
        return await current_scene.fallback(request_parser)
