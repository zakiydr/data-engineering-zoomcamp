FROM python:3.9-slim-bookworm

RUN apt-get update && apt-get install -y curl --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pandas sqlalchemy psycopg2-binary pyarrow

WORKDIR /app

# COPY ingest-data.py ingest-data.py 
COPY ingest-data.py ingest-data.py 

# ENTRYPOINT [ "python", "ingest-data.py" ]
ENTRYPOINT [ "python", "ingest-data.py" ]