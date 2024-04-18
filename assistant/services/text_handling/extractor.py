from fuzzywuzzy import fuzz
from core.config import fuzz_config, fasttext_config
from services.text_handling.model_loader import ft_model, spacy_model
import asyncio


class EntityExtractor:
    def __init__(self):
        self.movie_list_file = fuzz_config.movie_list_file

    async def load_movie_list(self, movie_list_file: str):
        movie_list = []
        loop = asyncio.get_event_loop()
        with open(movie_list_file, 'r') as file:
            while True:
                line = await loop.run_in_executor(None, file.readline)
                if not line:
                    break
                movie_list.append(line.strip())
        return movie_list

    async def extract_label(self, text: str):
        threshold = fasttext_config.threshold
        labels, probabilities = await asyncio.to_thread(ft_model.predict, text)

        if probabilities[0] >= threshold:
            predicted_label = labels[0]
        else:
            predicted_label = "not_in_label"
        return predicted_label

    async def extract_movies(self, text: str):
        best_match = None
        best_score = 0
        text_lower = text.lower()

        movie_list = await self.load_movie_list(self.movie_list_file)

        for movie in movie_list:
            movie_lower = movie.lower()
            similarity_score = fuzz.partial_ratio(text_lower, movie_lower)
            if similarity_score >= fuzz_config.threshold and similarity_score > best_score:
                best_match = movie
                best_score = similarity_score

        return best_match

    async def spacy_names(self, text: str):
        doc = spacy_model(text)
        for entity in doc.ents:
            if entity.label_ == "PER":
                return entity.text

    async def process_text_async(self, text: str):
        entities = {
            "text": text, "author": None, "film_name": None, "label": None}

        async def process_author():
            entities['author'] = await self.spacy_names(text)

        async def process_label():
            entities['label'] = await self.extract_label(text)

        async def process_film_name():
            entities["film_name"] = await self.extract_movies(text)

        await asyncio.gather(
            process_author(),
            process_label(),
            process_film_name()
        )

        return entities


async def get_extractor():
    return EntityExtractor()
