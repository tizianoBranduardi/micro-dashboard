import psycopg2
from sqlalchemy import create_engine

#Locals :

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5434/micro_dashboard')

# Containers :

# engine = create_engine('postgresql+psycopg2://postgres:postgres@micro-dashboard_db_1/micro_dashboard')

query_homepage = 'SELECT F.codice AS CodiceFattura, F.data AS DataFattura, A.codice AS CodiceArticolo, A.descrizione AS DescrizioneArticolo, A_F.quantita, A_F.prezzo\
                FROM fattura AS F\
                JOIN articolo_in_fattura AS A_F ON F.data = A_F.data_fattura_fk AND F.codice = A_F.codice_fattura_fk\
                JOIN articolo AS A ON A.codice = A_F.codice_articolo_fk AND A.descrizione = A_F.descrizione_articolo_fk\
                JOIN cliente AS C ON F.cliente_fk = C.codice_bms'

query_fatturato_cliente = 'WITH temp as (SELECT C.ragione_sociale, A_F.quantita * A_F.prezzo as total\
                FROM public.fattura AS F\
                JOIN public.articolo_in_fattura AS A_F ON F.data = A_F.data_fattura_fk AND F.codice = A_F.codice_fattura_fk\
                JOIN public.articolo AS A ON A.codice = A_F.codice_articolo_fk AND A.descrizione =A_F.descrizione_articolo_fk\
                JOIN public.cliente AS C ON F.cliente_fk = C.codice_bms)\
                SELECT ragione_sociale, SUM(total) as total\
                FROM temp AS T\
                GROUP BY T.ragione_sociale'

query_fatturato_settore = 'WITH temp as (SELECT C.settore, A_F.quantita * A_F.prezzo as total\
                        FROM public.fattura AS F\
                        JOIN public.articolo_in_fattura AS A_F ON F.data = A_F.data_fattura_fk AND F.codice = A_F.codice_fattura_fk\
                        JOIN public.articolo AS A ON A.codice = A_F.codice_articolo_fk AND A.descrizione =A_F.descrizione_articolo_fk\
                        JOIN public.cliente AS C ON F.cliente_fk = C.codice_bms)\
                        SELECT settore, SUM(total) as total\
                        FROM temp AS T\
                        GROUP BY T.settore'

query_fatturato_paese = 'WITH temp as (SELECT C.paesi, A_F.quantita * A_F.prezzo as total\
                        FROM public.fattura AS F\
                        JOIN public.articolo_in_fattura AS A_F ON F.data = A_F.data_fattura_fk AND F.codice = A_F.codice_fattura_fk\
                        JOIN public.articolo AS A ON A.codice = A_F.codice_articolo_fk AND A.descrizione =A_F.descrizione_articolo_fk\
                        JOIN public.cliente AS C ON F.cliente_fk = C.codice_bms)\
                        SELECT paesi, SUM(total) as total\
                        FROM temp AS T\
                        GROUP BY T.paesi'

query_fatturato_famiglia = 'WITH temp as (SELECT A.famiglia, A_F.quantita * A_F.prezzo as total\
                            FROM public.fattura AS F\
                            JOIN public.articolo_in_fattura AS A_F ON F.data = A_F.data_fattura_fk AND F.codice = A_F.codice_fattura_fk\
                            JOIN public.articolo AS A ON A.codice = A_F.codice_articolo_fk AND A.descrizione =A_F.descrizione_articolo_fk\
                            JOIN public.cliente AS C ON F.cliente_fk = C.codice_bms)\
                            SELECT famiglia, SUM(total) as total\
                            FROM temp AS T\
                            GROUP BY T.famiglia'