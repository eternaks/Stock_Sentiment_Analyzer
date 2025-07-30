import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(auth_plugin_map={'mysql_clear_password':None},host=os.getenv("db_endpoint"), user="admin", password=os.getenv("db_password"), port=3306, database="data", ssl_ca='data_pipeline/certs/global-bundle.pem', ssl_verify_identity=True, ssl_verify_cert=True)

c = conn.cursor()
c.execute("USE data")

def insert(ticker, polarity, confidence):
    # check for ticker existance in data
    c.execute("SELECT EXISTS(SELECT 1 FROM predictions WHERE ticker = '" + ticker + "')")

    # if not in data, insert row
    if not c.fetchone()[0]:
        c.execute("INSERT INTO predictions (ticker) VALUES ('" + ticker + "');")
        conn.commit()
    
    # update values
    c.execute("UPDATE predictions SET " + polarity + " = " + polarity + " + " + confidence + " WHERE ticker = '" + ticker + "'")
    c.execute("UPDATE predictions SET amt = amt + 1 WHERE ticker = '" + ticker + "'")
    conn.commit()