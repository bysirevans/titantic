import psycopg2
import pandas as pd

DBNAME = 'rfizardl'
USER = 'rfizardl'
PASSWORD = 'RQOnsyJfOrNYpnAv1j4myZgAj5Qlhb_L'
HOST = 'suleiman.db.elephantsql.com'

pg_conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST)
pg_curs = pg_conn.cursor()

def execute_query_pg(curs, conn, query):
    results = curs.execute(query)
    conn.commit()
    return results 

TITANIC_TABLE = '''
CREATE TABLE IF NOT EXISTS titanic_table(
    passenger_id SERIAL PRIMARY KEY,
    survived INT NOT NULL,
    pclass INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    sex VARCHAR(10) NOT NULL,
    age FLOAT NOT NULL,
    siblings_spouses_aboard INT NOT NULL,
    parents_children_aboard INT NOT NULL,
    fare FLOAT NOT NULL
);
'''

df = pd.read_csv('titanic.csv')
df['Name'] = df ['Name'].str.replace("'",'') 
if __name__ == '__main__':
    execute_query_pg(pg_curs, pg_conn, TITANIC_TABLE)

    records = df.values.tolist()

    for record in records:
        insert_statement = f'''
        INSERT INTO titanic_table(survived, pclass, name, sex, age, siblings_spouses_aboard, parents_children_aboard, fare)
        VALUES {(tuple(record))} 
        '''
        execute_query_pg(pg_curs, pg_conn, insert_statement)
