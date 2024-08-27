import pickle
import time

import nltk
import pandas as pd
from cocktail_scraper import CocktailScraper
from crawl import Crawler
from googletrans import Translator
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer


class TextProcessor:
    def __init__(self):
        nltk.download("wordnet")
        nltk.download("omw-1.4")
        self.lemmatizer = WordNetLemmatizer()
        self.translator = Translator()

    def translate_text(self, text):
        try:
            return self.translator.translate(text, src="pt", dest="en").text
        except Exception as e:
            return text

    def translate_batch(self, df, batch_size=10, sleep_time=1):
        translated_texts = []
        for start in range(0, len(df), batch_size):
            batch = df.iloc[start : start + batch_size]
            translated_batch = batch["how_to"].apply(self.translate_text)
            translated_texts.extend(translated_batch)
            time.sleep(sleep_time)
            # TODO: add logging
        return translated_texts

    def lemmatize_text(self, text):
        return self.lemmatizer.lemmatize(text)

    def process_data(self, data_path):
        try:
            df = pd.read_csv(f"{data_path}/cocktail_data.csv").astype(str)
        except Exception as e:
            return None

        df["how_to_translated"] = self.translate_batch(df)

        df["whole_text"] = df.apply(
            lambda row: f"{row.garnish} {row.how_to_translated} {row.comment} {row.history}", axis=1
        )
        df["whole_text"] = df["whole_text"].apply(self.lemmatize_text)

        try:
            df.to_csv(f"{data_path}/cocktail_data_silver.csv", index=False)
        except Exception as e:
            ...

        return df["whole_text"]


class ModelTrainer:
    def __init__(self, vectorizer=None):
        self.vectorizer = vectorizer or TfidfVectorizer(
            strip_accents="unicode", stop_words="english", lowercase=True
        )

    def train_model(self, model_path, text):
        tfidf_matrix = self.vectorizer.fit_transform(text)

        try:
            with open(f"{model_path}/vectorizer.pk", "wb") as f:
                pickle.dump(self.vectorizer, f)
            with open(f"{model_path}/tfidf_matrix.pk", "wb") as f:
                pickle.dump(tfidf_matrix, f)
        except Exception as e:
            ...

        return self.vectorizer, tfidf_matrix


def main(base_url, start_url):
    scraper = CocktailScraper()
    crawler = Crawler(base_url, start_url, crawl_limit=10)

    try:
        crawler.crawl(scraper)
    except Exception as e:
        return

    text_processor = TextProcessor()
    text = text_processor.process_data(crawler.data_path)
    if text is None:
        return

    model_trainer = ModelTrainer()
    model_trainer.train_model(crawler.model_path, text)

if __name__ == "__main__":
    main()
