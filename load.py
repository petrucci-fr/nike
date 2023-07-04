from sys import stdout
from collections import namedtuple
from enum import Enum
from typing import Callable, Dict, List

from pandas import DataFrame, read_sql

from sqlalchemy import text
from sqlalchemy.engine.base import Engine

from tqdm.auto import tqdm

from src.settings import QUERIES_PATH


QueryResult = namedtuple("QueryResult", ["query", "result"])

class QueryEnum(Enum):
    VENTAS = "sales"
    STOCK = "stock"


def read_query(query_name: str) -> str:
    """Read the query from the file.

    Args:
        query_file (str): The name of the file.

    Returns:
        str: The query.
    """
    with open(f"{QUERIES_PATH}/{query_name}.sql", "r") as f:
        sqL_file = f.read()
        sql = text(sqL_file)
    return sql

def query_sales(database: Engine) -> QueryResult:
    """Get the query for sales.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for sales.
    """
    query_name = QueryEnum.VENTAS.value
    query = read_query(QueryEnum.VENTAS.value)

    return QueryResult(query=query_name, result=read_sql(query, database))

def query_stock(database: Engine) -> QueryResult:
    """Get the query for stock.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for stock.
    """
    query_name = QueryEnum.STOCK.value
    query = read_query(QueryEnum.STOCK.value)

    return QueryResult(query=query_name, result=read_sql(query, database))

def get_all_queries() -> List[Callable[[Engine], QueryResult]]:
    """Get all queries.

    Returns:
        List[Callable[[Engine], QueryResult]]: A list of all queries.
    """
    return [
        query_sales,
        query_stock,
    ]

def run_queries(database: Engine) -> Dict[str, DataFrame]:
    """Transform data based on the queries. For each query, the query is executed and
    the result is stored in the dataframe.

    Args:
        database (Engine): Database connection.

    Returns:
        Dict[str, DataFrame]: A dictionary with keys as the query file names and
        values the result of the query as a dataframe.
    """
    all_queries = get_all_queries()

    query_results = {}    

    with tqdm(total=len(all_queries), 
                bar_format='{l_bar}{bar:40}{r_bar}', 
                desc='Loading Data...', 
                postfix='',
                unit=" queries", 
                colour='#37B6BD',
            ) as progress_bar:

        for query in all_queries:
            query_result = query(database)
            query_results[query_result.query] = query_result.result
            
            progress_bar.set_postfix_str(query_result.query)
            progress_bar.update(1)

        progress_bar.set_description('Done!')
        progress_bar.set_postfix_str('Completed')


    return query_results
