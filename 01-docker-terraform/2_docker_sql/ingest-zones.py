import argparse
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = "zones"
    
    csv_file = "taxi_zone_lookup.csv"
    
    df = pd.read_csv(csv_file)
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    
    print("Starting...")
    df.to_sql(name=table_name, con=engine, if_exists='replace')
    print("Finished")
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data zone to PostgreSQL")
    
    parser.add_argument('--user', help="Username for Postgres")
    parser.add_argument('--password', help="Password for Postgres")
    parser.add_argument('--host', help="host for Postgres")
    parser.add_argument('--port', help="port for Postgres")
    parser.add_argument('--db', help="db for Postgres")
    
    args = parser.parse_args()
    main(args)