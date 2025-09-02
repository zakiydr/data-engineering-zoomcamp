#!/usr/bin/env python


import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
import time
import pyarrow.parquet as pq

# print(args.accumulate(args.integers))




def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    
    table_name = "green_taxi_data"
    parquet_filename = url.split('/')[-1]
    os.system(f"curl -L {url} -o {parquet_filename}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    parquet_file = pq.ParquetFile(parquet_filename)
    engine.connect()
    df_empty = parquet_file.schema.to_arrow_schema().empty_table().to_pandas()
    df_empty.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
    print(f"Table '{table_name}' created successfully.")
    
    batch_iterator = parquet_file.iter_batches(batch_size=100000)
    print("Starting...")
    
    start_time = time.time()

    for i, batch in enumerate(batch_iterator):
        chunk_start_time = time.time()

        df_chunk = batch.to_pandas()

        df_chunk.to_sql(name=table_name, con=engine, if_exists="append", index=False)

        chunk_end_time = time.time()

        print(
            f" Ingested chunk {i+1}, took {chunk_end_time - chunk_start_time:.2f} seconds"
        )

    end_time = time.time()
    print(
        f"Finished ingesting all data. Total time: {end_time - start_time:.2f} seconds"
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest Parquet data to PostgreSQL")

    parser.add_argument("--user", help="Username for PostgreSQL")
    parser.add_argument("--password", help="Password for PostgreSQL")
    parser.add_argument("--host", help="Host for PostgreSQL")
    parser.add_argument("--port", help="port for PostgreSQL")
    parser.add_argument("--db", help="database for PostgreSQL")
    parser.add_argument("--table_name", help="Name of the table result destination")
    parser.add_argument("--url", help="url of the parquet file")

    args = parser.parse_args()
    
    main(args)
