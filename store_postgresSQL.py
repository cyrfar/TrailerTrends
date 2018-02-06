from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd

# Define a database name (we're using a dataset on births, so we'll call it birth_db)
# Set your postgres username/password, and connection specifics
user = 'YOUR_USERNAME' #input yout user name
password = 'YOUR_PASSWORD'     # change this
host     = 'localhost'
port     = '5432'            # default port that postgres listens on
dbname  = 'movie_db'