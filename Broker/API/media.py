import json
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool

load_dotenv()

dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

print(f"Connecting to database {dbname} at {host}:{port} with user {user}")

connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20, dbname=dbname, user=user, password=password, host=host, port=port
)


def get_connection():
    return connection_pool.getconn()


def release_connection(conn):
    connection_pool.putconn(conn)


def close_all_connections():
    connection_pool.closeall()


def registerAgent(message, aid, corporation):
    # Takes in a json object with aid, aip, aport, capacity(0,1,2), identifier(Unique string to ensure agent identity)
    message = json.loads(message)
    conn = get_connection()
    cursor = conn.cursor()
    update_query = """
    UPDATE agentstore
    SET aip = %s, aport = %s, capacity = %s, storage =%s, identifier = %s, corporation = %s
    WHERE aid = %s;
    """
    values = (
        message["aip"],
        message["aport"],
        message["capacity"],
        message["storage"],
        message["identifier"],
        corporation,
        aid,
    )
    print(values)
    cursor.execute(update_query, values)
    conn.commit()
    release_connection(conn)
    return {"message": "Agent registered"}


def get_agent_details_from_media(mid):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        m.aid, 
        a.keyid, 
        a.aip, 
        a.aport,
        k.pem_priv,
        k.agent_pem_pub
    FROM 
        media m
    JOIN 
        agentstore a ON m.aid = a.aid
    JOIN 
        keystore k ON a.aid = k.aid
    WHERE 
        m.mid = %s AND 
        a.verified = TRUE;
    """

    cursor.execute(query, (mid,))
    result = cursor.fetchone()

    release_connection(conn)

    return result


def get_avail_store_agents(corporation):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT aid, aport, aip, corporation 
    FROM agentstore
    WHERE verified = FALSE AND (capacity = 'dual' OR capacity = 'store')
    AND corporation = %s
    """
    cursor.execute(query, (corporation,))  # Note the comma to create a tuple
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    result = [dict(zip(column_names, row)) for row in rows]

    release_connection(conn)

    return result
