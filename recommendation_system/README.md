# **Cocktail Recommender with TF-IDF**

## **Table of Contents**
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Data](#data)
8. [Testing](#testing)
9. [Logging](#logging)
10. [Dockerization](#dockerization)
11. [Contributing](#contributing)
12. [License](#license)
13. [Contact Information](#contact-information)

---

## **Introduction**
This project is a Cocktail Recommender System that utilizes TF-IDF (Term Frequency-Inverse Document Frequency) to recommend cocktails based on user queries. It leverages data scraped from [Difford's Guide](https://www.diffordsguide.com), processed to provide relevant cocktail suggestions.

## **Project Structure**
- **app/**: Contains the FastAPI application code, including API routes and the recommendation logic.
- **data/**: Directory for storing the dataset and any intermediate processed files.
- **model/**: Directory for storing trained models and vectorizers.
- **scripts/**: Contains scripts for data scraping and preprocessing.
- **test/**: Includes unit tests for various components of the project.
- **logs/**: Directory for storing log files.
- **recommendation_system/**: Main project directory, includes the core logic and environment settings.

## **Features**
- **Cocktail Recommendations**: Suggests cocktails based on user input using a TF-IDF model.
- **API Integration**: Exposes the recommendation system via a FastAPI interface.
- **Data Scraping**: Automatically gathers cocktail data from Difford's Guide.
- **Dockerized**: Easily deployable via Docker for consistent environment management.
- **Logging and Testing**: Built-in support for logging and unit testing.

## **Installation**

### Prerequisites
- Python 3.8+ (Tested on 3.12.3)
- Docker (if using Docker)

### Steps
1. Clone the repository:
    ``` bash
   git clone https://github.com/Vigrel/NLP-rec-sys.git
   cd NLP-rec-sys
   ```

2. (Optional) Set up a virtual environment:
   ```bash
   cd recommendation_system
   python -m venv env
   source env/bin/activate
   # or 
   make venv
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # or 
   make install
   ```

4. Install script dependencies (if needed for data scraping):
   ```bash
   cd scripts
   python -m venv env_scripts
   source env_scripts/bin/activate
   pip install -r requirements.txt
   python get_data.py
   # or 
   make venv-scripts
   ```
   This environment resolves a conflict between FastAPI's dependencies and `googletrans` (httpx lib). If you already have the data, skip this step.

   You can adjust the amount of data gathered by modifying `craw_limit` in the `Crawl` class in [crawl.py](./scripts/crawl.py).

## **Usage**

### Prerequisites
To query the API, you need a chosen vectorizer and the TF-IDF matrix. These will match your query and generate recommendations. You can do this in two ways in [app.main.py](./app/main.py):

- **Pass Vectorizer and TF-IDF Matrix:**
   ```python
   tfidf = TfidfRecommender(
       df=your_data, 
       vectorizer=your_vectorizer, # TfidfVectorizer from scikit-learn
       tfidf_matrix= your_matrix
   )
   ```
   
- **Use Data to Generate the Vectorizer and TF-IDF Matrix:**
   ```python
   # Your files should be named cocktail_data.csv, vectorizer.pk, tfidf_matrix.pk
   # TODO: change the need of a fixed name. Sorry :(
   tfidf = TfidfRecommender.from_files(
       data_path="./data/example/",
       model_path="./model/example/"
   )
   ```

### Run/Use
To run the API, execute the following command:
```bash
python app/main.py
# or
make run
```

To get cocktail recommendations:

- Provide input via a GET request on your localhost:

```bash
curl localhost:8000/query?query=YOUR%20COCKTAIL%20PHRASE%20REQUIREMENTS
```

- Access FastAPI documentation at [localhost:8000/docs](http://localhost:8000/docs) to use the API interactively.

The recommender will return a list of cocktails matching your input.

## **Configuration**
Currently, the scripts require manual changes to certain variables, such as the file paths for the data and model files. Future updates will include modular scripts with flags and environment variables for easier configuration. Stay tuned for updates!

## **Data**
The cocktail data is scraped from [Difford's Guide](https://www.diffordsguide.com) using the scripts in the `scripts/` directory. The data is stored in the `data/` directory as a CSV file. It is then processed to translate all content to the same language and prepare it for the TF-IDF model.

## **Testing**
Unit tests are included in the `test/` directory. To run the tests, use the following command:

```bash
cd recommendation_system
pytest test/
# or
make test
```
This will execute the tests and display coverage information.

## **Logging**
Logging is configured in the `logs/logger.py` file. Logs are stored in the `logs/` directory by default. You can adjust the logging level in the configuration settings.

## **Dockerization**
To build and run the Docker container:

1. Build the Docker image:
   ```bash
   docker build -t cocktail-recommender .
   # or
   make docker-build
   ```

2. Run the container:
   ```bash
   docker run -p 9000:8888 cocktail-recommender
   # or 
   make docker-run
   ```
The application will be accessible at `http://localhost:9000`.

## **Contributing**
Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository (https://github.com/Vigrel/NLP-rec-sys.git).
2. Create a new branch:
   ```bash
   git switch -c nameInitials/featureDeveloped
   # Example: ve/crawlOptimization
   ```
3. Make your changes.
4. Commit your changes with a descriptive message:
   ```bash
   git commit -m 'feat: add new feature'
   ```
   Please follow the [Commit Patterns](./commit_pattern.md).
5. Push to the branch:
   ```bash
   git push origin nameInitials/featureDeveloped
   ```
6. Open a Pull Request (There’s no set pattern for PRs yet; please be descriptive about your work).

## **License**
This project is licensed under the MIT License - see the [LICENSE](./license.txt) file for details.

## **Contact Information**
For any questions, feel free to reach out to me at [viniciusge@al.insper.edu.br](mailto:viniciusge@al.insper.edu.br).