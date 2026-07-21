import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(auth_plugin_map={'mysql_clear_password':None},host=os.getenv("db_endpoint"), user="admin", password=os.getenv("db_password"), port=3306, database="data", ssl_ca='data_pipeline/certs/global-bundle.pem', ssl_verify_identity=True, ssl_verify_cert=True)
c = conn.cursor()
c.execute("USE data")
c.execute("SELECT * FROM predictions ORDER BY amt DESC LIMIT 20")

for row in c.fetchall():
    ticker = row[0]
    positives = row[1]
    neutrals = row[2]
    negatives = row[3]
    amt = row[5]
    rating = (positives-negatives) / (positives + neutrals + negatives)
    print("Ticker: " + ticker + " information")
    print("Positive rating: " + str(positives))
    print("Neutral rating: " + str(neutrals))
    print("Negative rating: " + str(negatives))
    print("Out of " + str(amt) + " post mentions")
    print("Overall rating: " + str(rating))
    print("")
    print("//////////////////////////////////////")
    print("")
    