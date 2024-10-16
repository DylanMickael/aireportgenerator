# Flask Project with Cohere API

This Flask project is designed to connect to an existing H2 database and utilize the Cohere API to generate product descriptions and conduct data analyses. The application is currently in the development phase and aims to streamline the process of deriving insights from stored data by leveraging advanced language processing capabilities.

## Prerequisites

- Python 3.7+
- Flask
- Cohere SDK
- H2 database
- A `config.ini` file containing your Cohere API key

## Installation and configuration

1. Clone the project repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. Install the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Create a config.ini file in the root directory of the project to store your API key and database configuration
    ```config.ini
    [API]
    cohere_api_key = #your_api_key
    
    [DATABASE]
    URL = #h2_database_path
    USER = #h2_database_user
    PASSWORD = #h2_database_password
    ```

## Running the application

Start the Flask application:
    ```bash
    python app.py
    ```