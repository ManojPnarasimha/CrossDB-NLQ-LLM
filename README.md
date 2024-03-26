# Cross-Database Data Retrieval with Natural Language Query Using LLM

This project demonstrates how to perform cross-database data retrieval using natural language queries with Large Language Models (LLM). It involves querying two separate PostgreSQL databases, "user_db" and "user_info", and retrieving relevant information based on user input.

**#Installation**

1. Clone the repository:

   ```bash
   git clone https://github.com/ManojPnarasimha/CrossDB-NLQ-LLM.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure that your PostgreSQL databases "user_db" and "user_info" are properly set up and accessible or Any Other data base of .

2. Modify the `.env` file and set the `API_KEY` variable to your Google API key.

3. Run the `main.py` script:

   ```bash
   python main.py
   ```

4. Follow the prompts to enter your query. You can type 'exit' to quit.

## Description

This project includes the following components:

- `main.py`: The main script that initializes the database connections, sets up the LLM, defines the tools for querying databases, and runs the aggregator agent to retrieve data based on user input.

- `langchain_community.utilities.sql_database`: Module containing utilities for working with SQL databases.

- `langchain_experimental.sql.base`: Module containing the base classes for working with SQL databases in LangChain Experimental.

- `langchain.agents`: Module containing classes and functions for initializing agents and tools.

- `langchain_google_genai`: Module for integrating Google Generative AI.

