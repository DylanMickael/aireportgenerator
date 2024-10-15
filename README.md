# Flask Project with Cohere API

This Flask project allows you to generate product descriptions using the Cohere API. This document explains how to configure the `config.ini` file necessary for the application to function.

## Prerequisites

- Python 3.7+
- Flask
- Cohere SDK
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
3. Create a config.ini file in the root directory of the project to store your Cohere API key
    ```config.ini
    [API]
    cohere_api_key = #your_api_key
    ```

## Running the application

Start the Flask application:
    ```bashpip
    python app.py
    ```