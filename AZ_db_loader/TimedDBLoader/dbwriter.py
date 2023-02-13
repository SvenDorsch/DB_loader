import pyodbc
import numpy as np
import pandas as pd

from sqlalchemy import create_engine



def insert_random_number():
    """
    Establishes connection to database and adds random number entry
    """

    SERVER = 'functions-test-db-server.database.windows.net'
    USER = ''
    PWD = ''
    DRIVER = 'ODBC Driver 18 for SQL Server'

    connection_str = f'mssql+pyodbc://{USER}:{PWD}@{SERVER}:1433/db?driver={DRIVER}'
    engine = create_engine(connection_str)

    df = pd.DataFrame(columns=['random_number'], data=np.random.randint(100, size=(1)))
    df.to_sql('randomNumbers', engine, if_exists='append', index=False)



if __name__ == "__main__":
    insert_random_number()