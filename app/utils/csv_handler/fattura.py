import psycopg2
import pandas as pd
from utils.db_connector import engine
from utils.csv_handler.date_format import format_date
pd.options.mode.chained_assignment = None  # default='warn'

csv_columns = ['nro_ftt', 'data_reg_ftt', 'codice_cli']
db_attributes_map = {'nro_ftt': 'codice', 'data_reg_ftt': 'data', 'codice_cli': 'cliente_fk'}
check_query = "SELECT codice, data FROM fattura"


def clean_df_for_fattura(df):
    try:

        fattura = df[csv_columns]
        fattura = fattura.drop_duplicates(ignore_index=True)
        fattura = fattura.rename(
            columns=db_attributes_map)
        # Drop null values, convert nro_ftt into integer and format data for data_reg_ftt
        fattura = fattura[
            pd.to_numeric(fattura['codice'], errors='coerce').notnull()].reset_index(drop=True)
        fattura['codice'] = fattura['codice'].astype(int).apply(lambda x: str(x) + ' / F')
        fattura['data'] = fattura['data'].apply(lambda x: format_date(x))
        fattura['data'] = pd.to_datetime(fattura['data'])
        return fattura.dropna()

    except Exception as error:
        print(error, flush=True)


def insert_fattura(fattura):
    try:
        res = fattura.to_sql(name='fattura', con=engine, schema='public', if_exists='append', index=False)
        return 'Inserite ' + str(res) + ' nuove fatture'
    except Exception as e:
        #print(e, flush=True)
        return 'Inserite 0 nuove fatture'
