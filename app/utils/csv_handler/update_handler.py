from utils.db_connector import engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, scoped_session
import pandas as pd


def insert_or_ignore(df, table, keys, fields):
    df.to_sql('temp_table', engine, if_exists='replace')
    table = 'public.'+table
    keys = " ".join(keys)
    keys = keys.replace(" ", ",")

    fields = " ".join(fields)
    fields = fields.replace(" ", ",")

    sql = ("INSERT INTO %s (%s) SELECT %s FROM public.temp_table ON CONFLICT (%s) DO NOTHING;"
           % (table, fields, fields, keys))

    query = text(sql)

    print(query)
    Session = scoped_session(sessionmaker(bind=engine))
    s = Session()
    result = s.execute(query)
    print(result)
    with engine.connect() as conn:
        conn.execute(query).execution_options(autocommit=True)
    # for result in res:
    #     print(result)
    # if not res:
    #     amount_of_rows = 0
    # else:
    #     amount_of_rows = res
    # print("Res")
    # print(amount_of_rows)
    return 123
