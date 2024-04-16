import fasttext
import spacy

from core.config import fasttext_config


ft_model = fasttext.train_supervised(
    input=fasttext_config.intents_file,
    lr=fasttext_config.lr,
    epoch=fasttext_config.epoch,
    wordNgrams=fasttext_config.wordNgrams)

spacy_model = spacy.load("ru_core_news_sm")
