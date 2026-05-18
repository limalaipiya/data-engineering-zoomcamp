import io
import pandas as pd
from sqlalchemy import create_engine, text
from tqdm import tqdm
import click


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for ingestion')
@click.option('--target-taxi-table', default='green_trip_data', help='Target table name')
@click.option('--target-zone-table', default='zone_data', help='Target table name')
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize, target_taxi_table, target_zone_table):
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    run_ny_taxi(engine, year, month, chunksize, target_taxi_table)
    run_zones(engine, target_zone_table)

def copy_df_to_sql(df, engine, table_name):
    df.columns = df.columns.str.lower()  # เพิ่มบรรทัดนี้
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)

    conn = engine.raw_connection()
    try:
        cursor = conn.cursor()
        cursor.copy_expert(
            f"COPY {table_name} ({', '.join(df.columns)}) FROM STDIN WITH (FORMAT CSV)",
            buffer
        )
        conn.commit()
    finally:
        conn.close()


def run_ny_taxi(engine, year, month, chunksize, target_taxi_table):
    prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    url = f'{prefix}/green_tripdata_{year}-{month:02d}.parquet'

    df_iter = pd.read_parquet(
        url,
        engine='pyarrow'
    )

    df_iter.head(0).rename(columns=str.lower).to_sql(
        name=target_taxi_table,
        con=engine,
        if_exists='replace',
        index=False
    )
    
    for i in tqdm(range(0, len(df_iter), chunksize)):
        df_chunk = df_iter.iloc[i:i+chunksize]
        copy_df_to_sql(df_chunk, engine, target_taxi_table)


def run_zones(engine, target_zone_table):
    url = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv'
    df_zones = pd.read_csv(url)
    df_zones = df_zones.rename(columns=str.lower)
    df_zones.head(0).to_sql(
        name=target_zone_table, 
        con=engine, 
        if_exists='replace',
        index=False
    )

    copy_df_to_sql(df_zones, engine, target_zone_table)


if __name__ == '__main__':
    main()