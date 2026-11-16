import pandas as pd

from utils.sql_loader import load_sql


def extract_chunks(connection, etapa, sql_file, params=None, chunksize=15000):

    query = load_sql(etapa, sql_file)

    chunks = pd.read_sql(
        query,
        connection,
        params=params,
        chunksize=chunksize
    )

    for chunk in chunks:
        yield chunk


def extract_dataframe(connection, etapa, sql_file, params=None):

    query = load_sql(etapa, sql_file)

    return pd.read_sql(
        query,
        connection,
        params=params
    )