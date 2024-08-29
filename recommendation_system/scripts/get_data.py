import logging
import pickle
import time

import nltk
import pandas as pd
from cocktail_scraper import CocktailScraper
from crawl import Crawler
from googletrans import Translator
from logs.logger import Logger
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

Logger.setup_log(log_level=logging.INFO, local_dir="./logs")
logger = logging.getLogger(__name__)


class TextProcessor:
    def __init__(self):
        logger.info("Downloading nltk and translator extensions")
        nltk.download("wordnet")
        nltk.download("omw-1.4")
        self.lemmatizer = WordNetLemmatizer()
        self.translator = Translator()

    def translate_text(self, text):
        logger.info(text)
        try:
            translated_text = self.translator.translate(text, src="pt", dest="en").text
            logger.info(translated_text)
            logger.debug(f"Translated text: {text} -> {translated_text}")
            return translated_text
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text

    def translate_batch(self, df, batch_size=3, sleep_time=1):
        translated_texts = []
        for start in range(0, len(df), batch_size):
            batch = df.iloc[start : start + batch_size]
            translated_batch = batch["how_to"].apply(self.translate_text)
            translated_texts.extend(translated_batch)
            logger.info(f"Translated batch {start} to {start + batch_size}")
            time.sleep(sleep_time)
        return translated_texts

    def lemmatize_text(self, text):
        lemmatized_text = self.lemmatizer.lemmatize(text)
        logger.debug(f"Lemmatized text: {text} -> {lemmatized_text}")
        return lemmatized_text

    def process_data(self, data_path):
        try:
            df = pd.read_csv(f"{data_path}/cocktail_data.csv").astype(str)
            logger.info(f"Loaded data from {data_path}/cocktail_data.csv")
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            return None

        df["how_to_translated"] = self.translate_batch(df)

        df["whole_text"] = df.apply(
            lambda row: f"{row.garnish} {row.how_to_translated} {row.comment} {row.history}",
            axis=1,
        )
        df["whole_text"] = df["whole_text"].apply(self.lemmatize_text)

        try:
            output_path = f"{data_path}/cocktail_data_silver.csv"
            df.to_csv(output_path, index=False)
            logger.info(f"Saved processed data to {output_path}")
        except Exception as e:
            logger.error(f"Failed to save processed data: {e}")

        return df["whole_text"]


class ModelTrainer:
    def __init__(self, vectorizer=None):
        self.vectorizer = vectorizer or TfidfVectorizer(
            strip_accents="unicode", stop_words="english", lowercase=True
        )

    def train_model(self, model_path, text):
        try:
            tfidf_matrix = self.vectorizer.fit_transform(text)
            logger.info("TF-IDF matrix created successfully")

            with open(f"{model_path}/vectorizer.pk", "wb") as f:
                pickle.dump(self.vectorizer, f)
            with open(f"{model_path}/tfidf_matrix.pk", "wb") as f:
                pickle.dump(tfidf_matrix, f)
        except Exception as e:
            logger.error(f"Model training failed: {e}")

        return self.vectorizer, tfidf_matrix


def main(base_url, start_url):
    logger.info("Starting scraping")
    scraper = CocktailScraper()
    crawler = Crawler(base_url, start_url, crawl_limit=3)

    try:
        crawler.crawl(scraper)
        logger.info("Crawling completed")
    except Exception as e:
        logger.error(f"Crawling failed: {e}")
        return

    text_processor = TextProcessor()
    text = text_processor.process_data(crawler.data_path)
    if text is None:
        logger.warning("No text data to process, exiting")
        return

    model_trainer = ModelTrainer()
    model_trainer.train_model(crawler.model_path, text)

    logger.info("Main process completed, exiting")


if __name__ == "__main__":
    main()
