import re
from typing import Dict, Tuple

import pandas as pd
from bs4 import BeautifulSoup


class CocktailScraper:
    def __init__(self):
        self.df = pd.DataFrame(
            columns=[
                "drink_title",
                "drink_glass",
                "garnish",
                "how_to",
                "comment",
                "history",
                "nutrition",
                "alcohol_content",
                "path"
            ]
        )

    def extract_cocktail_info(self, text: str) -> Dict[str, str]:
        text = re.sub(r"\s+", " ", text)
        patterns = {
            "drink_glass": r"Servir em (.*?) Fotografado",
            "garnish": r"Decoração: (.*?) Como fazer:",
            "how_to": r"Como fazer: (.*?) Loading...",
            "comment": r"Comentários: (.*?) História:",
            "history": r"História: (.*?) Nutrition:",
            "nutrition": r"Nutrition: (.*?) cal",
            "alcohol_content": r"Alcohol content: (.*?) grams of pure alcohol",
        }

        extracted_info = {}

        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                extracted_info[key] = match.group(1).strip()
            else:
                extracted_info[key] = None

        return extracted_info

    def get_next_cocktails(self, soup: BeautifulSoup) -> Tuple[str, str]:
        information_div = soup.find_all(
            "a", class_="cell small-6 colour-inherit opacity-hover", href=True
        )
        if len(information_div) < 2:
            return "", ""
        return (information_div[0].get("href"), information_div[1].get("href"))

    def scrape_cocktail_details(self, soup: BeautifulSoup, current_url:str) -> None:
        information_div = soup.find(
            "article",
            class_="cell long-form long-form--small long-form--inline-paragraph pad-bottom",
        ).text.strip()
        cocktail_data = self.extract_cocktail_info(information_div)

        cocktail_data["drink_title"] = current_url.split("/")[-1]
        cocktail_data["path"] = current_url

        self.df.loc[len(self.df)] = cocktail_data


if __name__ == "__main__":
    scraper = CocktailScraper()
