import pandas as pd
from sqlalchemy import create_engine
import click

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass',default='root',help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, help='postgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')

def ingest_data(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):
    """Ingest data into PostgreSQL database"""
    print(f"Connecting to PostgreSQL database {pg_db} at {pg_host}:{pg_port} as user {pg_user}")
    uri = f"postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    engine = create_engine(uri)


    prefix= 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url= prefix + 'yellow_tripdata_2021-01.csv.gz'
    dtype={
        "VendorID": "Int64",
        "passenger_count":"float64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra":"float64",
        "mta_tax":"float64",
        "tip_amount":"float64",
        "improvement_surcharge":"float64",
        "total_amount":"float64",
        "congestion_surcharge":"float64"
        }

    parse_dates=[
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
        ]
    
    print("Downloading and chunking data...")
    df_iter = pd.read_csv(
        url, 
        dtype=dtype, 
        parse_dates=parse_dates, 
        iterator=True, 
        chunksize=10000,
        low_memory=False # <-- Add this line right here
    )







    first=True

    for df_chunk in df_iter:

        if first:
            df_chunk.head(0).to_sql(name=target_table,con=engine, if_exists="replace")
            
            first=False
            print(f"Empty table '{target_table}' created successfully")


        df_chunk.to_sql(name=target_table, con=engine, if_exists="append")
        print(f"inserted a chunk of {len(df_chunk)} rows....")

    print("Finished ingesting all data!") 

if __name__ == "__main__":
    ingest_data()       










