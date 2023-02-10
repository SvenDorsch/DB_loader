"""
Exemplary DB read and write operations using python, pandas and pyobdc.
Following the code in https://github.com/mkempers/howto-sqlazure-pandas/
"""

import pyodbc
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

from secret_credentials import db_credentials  # Contains server name and user credentials

if __name__ == "__main__":

    # Get DB credentials with read and write access:
    SERVER = db_credentials.get('server')
    USER = db_credentials.get('user')
    PWD = db_credentials.get('password')
    DRIVER = 'ODBC Driver 18 for SQL Server'

    # Prepare a dataframe containing 5 random numbers:
    df = pd.DataFrame(columns=['random_data'], data=np.random.randint(100, size=(5)))


    ## Prepare server connection ##
    connection_str = f'mssql+pyodbc://{USER}:{PWD}@{SERVER}:1433/db?driver={DRIVER}'
    engine = create_engine(connection_str)


    ## Write/append to database ##
    df.to_sql('test_table', engine, if_exists='append', index=False)
    # Note that in rpder to create a new table if not exists, the user must
    # have permission to create a table.


    ## Read from database ##
    query = 'SELECT * FROM test_table'
    dfsql = pd.read_sql(query, engine)

    print(dfsql.tail())

