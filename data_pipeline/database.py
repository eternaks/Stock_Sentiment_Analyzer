import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# submission stream sql connection
conn_sub = pymysql.connect(auth_plugin_map={'mysql_clear_password':None},host=os.getenv("db_endpoint"), user="admin", password=os.getenv("db_password"), port=3306, database="data", ssl_ca='data_pipeline/certs/global-bundle.pem', ssl_verify_identity=True, ssl_verify_cert=True)
# comment steam sql connection
conn_com = pymysql.connect(auth_plugin_map={'mysql_clear_password':None},host=os.getenv("db_endpoint"), user="admin", password=os.getenv("db_password"), port=3306, database="data", ssl_ca='data_pipeline/certs/global-bundle.pem', ssl_verify_identity=True, ssl_verify_cert=True)


submission_cur = conn_sub.cursor()
comment_cur = conn_com.cursor()

submission_cur.execute("USE data")
comment_cur.execute("USE data")

def insert(ticker, polarity, confidence, iscom):
    global conn_sub, submission_cur, conn_com, comment_cur
    conn = conn_sub
    c = submission_cur
    if iscom == 1:
        conn = conn_com
        c = comment_cur
    
    try:
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
    except:
        if iscom:
            print("comment sql connection failed, reattempting connection")
            conn_com = pymysql.connect(auth_plugin_map={'mysql_clear_password':None},host=os.getenv("db_endpoint"), user="admin", password=os.getenv("db_password"), port=3306, database="data", ssl_ca='data_pipeline/certs/global-bundle.pem', ssl_verify_identity=True, ssl_verify_cert=True)
            comment_cur = conn_com.cursor()
            comment_cur.execute("USE data")
            print("connection reestablished")
        else:
            print("submission sql connection failed, reattempting connection")
            conn_sub = pymysql.connect(auth_plugin_map={'mysql_clear_password':None},host=os.getenv("db_endpoint"), user="admin", password=os.getenv("db_password"), port=3306, database="data", ssl_ca='data_pipeline/certs/global-bundle.pem', ssl_verify_identity=True, ssl_verify_cert=True)
            submission_cur = conn_sub.cursor()
            submission_cur.execute("USE data")
            print("connection reestablished")