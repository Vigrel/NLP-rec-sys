import pickle

import pandas as pd
from cocktail_scraper import CocktailScraper
from crawl import Crawler
from sklearn.feature_extraction.text import TfidfVectorizer

if __name__ == "__main__":
    base_url = ""
    start_url = ""
    scraper = CocktailScraper()
    crawler = Crawler(base_url, start_url, crawl_limit=10)
    crawler.crawl(scraper)

    df = pd.read_csv(f"{crawler.data_path}/cocktail_data.csv")
    df = df.astype(str)
    df["whole_text"] = df.garnish + " " + df.comment + " " + df.history

    vectorizer = TfidfVectorizer(
        strip_accents="unicode", stop_words="english", lowercase=True
    )
    tfidf_matrix = vectorizer.fit_transform(df.whole_text)

    with open(f"{crawler.model_path}/vectorizer.pk", "wb") as f:
        pickle.dump(vectorizer, f)

    with open(f"{crawler.model_path}/tfidf_matrix.pk", "wb") as f:
        pickle.dump(tfidf_matrix, f)
