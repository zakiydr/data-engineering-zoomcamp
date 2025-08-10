#!/usr/bin/env python

import argparse
import pandas as pd
from sqlalchemy import create_engine
import time
import pyarrow.parquet as pq

table_name = "yellow_taxi_data"
parquet_filename = "yellow_tripdata_2021-01.parquet"

engine = create_engine("postgresql://root:root@localhost:5433/ny_taxi")

df = pd.read_parquet("yellow_tripdata_2021-01.parquet", engine="pyarrow")
df.head()


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
print(f"Finished ingesting all data. Total time: {end_time - start_time:.2f} seconds")
