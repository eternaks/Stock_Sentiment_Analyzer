import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# only these column names are ever allowed to be interpolated into SQL,
# since pymysql can't parameterize identifiers
VALID_POLARITY_COLUMNS = {"Positive", "Neutral", "Negative"}


def connect():
    return pymysql.connect(
        auth_plugin_map={'mysql_clear_password': None},
        host=os.getenv("db_endpoint"),
        user="admin",
        password=os.getenv("db_password"),
        port=3306,
        database="data",
        ssl_ca='data_pipeline/certs/global-bundle.pem',
        ssl_verify_identity=True,
        ssl_verify_cert=True,
    )


# submission stream sql connection
conn_sub = connect()
# comment stream sql connection
conn_com = connect()

submission_cur = conn_sub.cursor()
comment_cur = conn_com.cursor()

submission_cur.execute("USE data")
comment_cur.execute("USE data")


def insert(ticker, polarity, confidence, iscom):
    global conn_sub, submission_cur, conn_com, comment_cur

    if polarity not in VALID_POLARITY_COLUMNS:
        raise ValueError(f"Unexpected polarity column: {polarity!r}")

    conn = conn_sub
    c = submission_cur
    if iscom == 1:
        conn = conn_com
        c = comment_cur

    try:
        # check for ticker existance in data
        c.execute("SELECT EXISTS(SELECT 1 FROM predictions WHERE ticker = %s)", (ticker,))

        # if not in data, insert row
        if not c.fetchone()[0]:
            c.execute("INSERT INTO predictions (ticker) VALUES (%s)", (ticker,))
            conn.commit()

        # update values (polarity is validated above against a fixed whitelist,
        # since column names can't be passed as query parameters)
        c.execute(
            f"UPDATE predictions SET {polarity} = {polarity} + %s WHERE ticker = %s",
            (confidence, ticker),
        )
        c.execute("UPDATE predictions SET amt = amt + 1 WHERE ticker = %s", (ticker,))
        conn.commit()
    except pymysql.MySQLError:
        if iscom:
            print("comment sql connection failed, reattempting connection")
            conn_com = connect()
            comment_cur = conn_com.cursor()
            comment_cur.execute("USE data")
            print("connection reestablished")
        else:
            print("submission sql connection failed, reattempting connection")
            conn_sub = connect()
            submission_cur = conn_sub.cursor()
            submission_cur.execute("USE data")
            print("connection reestablished")
