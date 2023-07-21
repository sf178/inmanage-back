import os
import pandas as pd
import requests
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime

# get current date
now = datetime.now()

# create file path based on current date
# path = f"{now.year}/{now.strftime('%m/%d')}/"
path = 'D:/inmanage-site/test_backend/actives/actives_scripts/market_prices/collector/quotes/2023/03/31/'
# create file name patterns
'''file_name_patterns = [
    f"{now.year}-{now.strftime('%m')}-{now.strftime('%d')}-stock-bonds.csv",
    f"{now.year}-{now.strftime('%m')}-{now.strftime('%d')}-stock-shares.csv",
    f"{now.year}-{now.strftime('%m')}-{now.strftime('%d')}-stock-index.csv",
    f"{now.strftime('%Y/%m/%d')}-stock-bonds.csv",
    f"{now.strftime('%Y/%m/%d')}-stock-shares.csv",
    f"{now.strftime('%Y/%m/%d')}-stock-index.csv"
]'''
file_name_patterns = [
    f"2023-03-31-stock-bonds.csv"
]
# columns to keep

# columns to keep for bonds and shares files
columns_to_keep_bonds_shares = ["SHORTNAME", "OPEN", "LOW", "HIGH", "MARKETPRICE2", "MARKETPRICE3"]

# columns to keep for index files
columns_to_keep_index = ["SHORTNAME", "OPEN", "LOW", "HIGH"]
dataframes = []

for file in os.listdir(path):
    if file.endswith(".csv"):
        # Get file type
                # Define columns to keep based on file type
        if "stock-bonds.csv" in file:
            columns = ["SHORTNAME", "SECID", "OPEN", "LOW", "HIGH", "MARKETPRICE2", "MARKETPRICE3"]
        elif "stock-shares.csv" in file:
            columns = ["SHORTNAME", "SECID", "OPEN", "LOW", "HIGH", "MARKETPRICE2", "MARKETPRICE3"]
        elif "stock-index.csv" in file:
            columns = ["SHORTNAME", "OPEN", "LOW", "HIGH"]
        else:
            continue

        # Read in CSV file
        df = pd.read_csv(os.path.join(path, file), usecols=columns)

        # Convert dataframe to JSON
        data = df.to_json(orient="records")
        #print(data)

        # Send data as API call to Postgres
        url = "http://127.0.0.1:8000/actives/bonds/"
        del_prev = "http://127.0.0.1:8000/actives/bonds/del"
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(del_prev)
        if response.status_code == 204:
            print('All objects deleted successfully.')
        else:
            print(f'Error deleting objects. Status code: {response.status_code}')
        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 200:
            print(f"Error sending data for file {file}")
        else:
            print(f"Data sent successfully for file {file}")

'''for file_name in file_name_patterns:
    file_path = path # + file_name
    print(file_path)
    try:
        if "stock-bonds.csv" in file_name or "stock-shares.csv" in file_name:
            df = pd.read_csv(file_path, usecols=columns_to_keep_bonds_shares)
            # print(df)
        elif "stock-index.csv" in file_name:
            df = pd.read_csv(file_path, usecols=columns_to_keep_index)
            # print(df)
        else:
            print('not found')
            continue
        print(df)

        # print(final_df)
        engine = create_engine('postgresql://postgres:samara63@localhost:5432/inmanage')
        conn = engine.connect()
        print(conn)
        df.to_sql('actives_bonds', conn, if_exists='append', index=False)
    except FileNotFoundError:
        # if file is not found, continue to the next file
        print('popa')
        continue'''


# send dataframe to postgres database


# close database connection
# conn.close()