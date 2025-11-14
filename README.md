A-SDLC Synthetic E-commerce Dataset

This repository provides a small synthetic e-commerce dataset along with helper scripts for generating CSVs, loading them into SQLite, and running analytical queries.


Project Structure

-data/ – generated CSV files (users.csv, products.csv, orders.csv, order_items.csv, payments.csv) plus generate_data.py.
-ingest.py – creates ecommerce.db, defines tables, and loads the CSV files using pandas.
-query.sql – join query combining all entities.
-run_query.py – executes query.sql against ecommerce.db and prints the result set.

Prerequisites

-Python 3.8+
-pip install pandas


Usage
-Generate data (optional if CSVs already exist)
-python data/generate_data.py
-Load data into SQLite
-python ingest.py


This creates/overwrites ecommerce.db in the project root and prints Ingestion complete.


Run the join query

python run_query.py


Outputs the joined table defined in query.sql.

Customization


Adjust record counts or value ranges by editing data/generate_data.py.
Modify query.sql to explore other questions, then re-run run_query.py.



License
This dataset and scripts are provided for demonstration and testing purposes. Use freely within your projects.***
