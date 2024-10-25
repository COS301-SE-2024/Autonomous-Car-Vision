from http import client

from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv
import json
import os
import base64
import psycopg2
import httpx
from fastapi import HTTPException

load_dotenv()

def obol():
    print(">>> Coin for the ferry man?")
    print("Generating Server side RSA key pair")
    init_key_pair = asymmetric()
    print("RSA KEY PAIR: ", init_key_pair)

    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    print(f"Connecting to database {dbname} at {host}:{port} with user {user}")

    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO keystore (init_key, initkey_validation)
    VALUES (%s, %s)
    RETURNING aid;
    """
    values = (init_key_pair["private"].decode("utf-8"), False)
    cursor.execute(insert_query, values)
    aid = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()
    print("Obol complete\n\n")
    return {"aid": aid, "public": init_key_pair["public"]}


def asymmetric():
    print(">>> Asymmetric key generation in progress")

    server_private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    server_public_key = server_private_key.public_key()

    private_pem = server_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_pem = server_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    print("Private key in PEM format:")
    print(private_pem.decode("utf-8"))
    print("Public key in PEM format:")
    print(public_pem.decode("utf-8"))
    print()
    return {"public": public_pem, "private": private_pem}


def asymmetric_decryption(aid, message):
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    print(f"Connecting to database {dbname} at {host}:{port} with user {user}")

    try:
        with psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        ) as conn:
            with conn.cursor() as cursor:
                select_query = """
                SELECT init_key FROM keystore
                WHERE aid = %s;
                """
                cursor.execute(select_query, (aid,))
                priv_key = cursor.fetchone()[0]

                print("Private key in PEM format:")
                print(priv_key)
                private_key = serialization.load_pem_private_key(
                    priv_key.encode(), password=None, backend=default_backend()
                )

                encrypted_symmetric_key = base64.b64decode(message["encrypted_key"])
                encrypted_data = base64.b64decode(message["encrypted_data"])
                iv = base64.b64decode(message["iv"])

                symmetric_key = private_key.decrypt(
                    encrypted_symmetric_key,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None,
                    ),
                )

                cipher = Cipher(
                    algorithms.AES(symmetric_key),
                    modes.CFB(iv),
                    backend=default_backend(),
                )
                decryptor = cipher.decryptor()
                decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

                decrypted_message = decrypted_data.decode("utf-8")
                decrypted_json = json.loads(decrypted_message)

                print("Decrypted message:", decrypted_json)
                return {"aid": aid, "public": decrypted_json}

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def elyptic(encoding):
    print(">>> Generating ECDH key pair")
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    if encoding:
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        print(">>> Elyptic keys encoded to pem format")
        print("Private Key:")
        print(private_pem.decode("utf-8"))

        print("Public Key:")
        print(public_pem.decode("utf-8"))

        return {"private": private_key, "public": public_key}

    print(">>> Elyptic keys not encoded to pem format")
    print("Private Key:")
    print(private_key)

    print("Public Key:")
    print(public_key)

    return {"private": private_key, "public": public_key}


def agentRegistration():
    print(">>> Registering agent")


def encrypt_message(public_key_pem, public_key):
    if isinstance(public_key_pem, bytes):
        public_key_pem = public_key_pem.decode("utf-8")

    public_key = serialization.load_pem_public_key(
        public_key_pem.encode("utf-8"), backend=default_backend()
    )
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    encrypted_message = public_key.encrypt(
        public_key_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    encrypted_message_base64 = base64.b64encode(encrypted_message).decode("utf-8")
    return encrypted_message_base64


def store_agent_keys(aid, ecdh_pub, rsa_pub):
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    cursor = conn.cursor()

    update_query = """
    UPDATE keystore
    SET pem_pub = %s, initkey_validation = TRUE
    WHERE aid = %s;
    """
    values = (ecdh_pub.decode("utf-8"), aid)
    cursor.execute(update_query, values)
    conn.commit()

    cursor.close()
    conn.close()


def generate_broker_ecdh_keys(aid, agent_rsa_pub_pem):
    broker_ecdh_keys = elyptic(True)
    broker_private = broker_ecdh_keys["private"]
    broker_public = broker_ecdh_keys["public"]

    broker_private_pem = broker_private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    broker_public_pem = broker_public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    cursor = conn.cursor()

    update_query = """
    UPDATE keystore
    SET pem_priv = %s, initkey_validation = TRUE, pem_pub = %s
    WHERE aid = %s;
    """
    print("Broker private", broker_private_pem)
    values = (broker_private_pem, broker_public_pem, aid)
    cursor.execute(update_query, values)
    conn.commit()

    cursor.close()
    conn.close()

    encrypted_broker_ecdh_pub = encrypt_messageecdh(
        agent_rsa_pub_pem, broker_public_pem
    )
    return {
        "aid": aid,
        "ecdh_public_encrypted": encrypted_broker_ecdh_pub,
        "ecdh_private": broker_private_pem,
        "ecdh_public": broker_public_pem,
    }


def encrypt_messageecdh(rsa_public_key_pem, ecdh_public_key_pem):
    if isinstance(rsa_public_key_pem, bytes):
        rsa_public_key_pem = rsa_public_key_pem.decode("utf-8")

    rsa_public_key = serialization.load_pem_public_key(
        rsa_public_key_pem.encode("utf-8"), backend=default_backend()
    )

    encrypted_message = rsa_public_key.encrypt(
        ecdh_public_key_pem.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    encrypted_message_base64 = base64.b64encode(encrypted_message).decode("utf-8")
    return encrypted_message_base64


def get_session(private_key, peer_public_key):
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    session_key = HKDF(
        algorithm=hashes.SHA256(), length=32, salt=None, info=b"session key"
    ).derive(shared_key)
    return session_key


def elyptic_encryptor(session_key, plaintext):
    iv = os.urandom(16)
    cipher = Cipher(
        algorithms.AES(session_key), modes.CFB(iv), backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode("utf-8")


def elyptic_decryptor(session_key, encrypted_message):
    encrypted_message_bytes = base64.b64decode(encrypted_message)
    iv = encrypted_message_bytes[:16]
    ciphertext = encrypted_message_bytes[16:]
    cipher = Cipher(
        algorithms.AES(session_key), modes.CFB(iv), backend=default_backend()
    )
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode("utf-8")


def getECDH(aid):
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    cursor = conn.cursor()

    select_query = """
    SELECT pem_priv, pem_pub, agent_pem_pub
    FROM keystore
    WHERE aid = %s;
    """
    cursor.execute(select_query, (aid,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        pem_priv, pem_pub, agent_pem_pub = result
        return {
            "pem_priv": pem_priv,
            "pem_pub": pem_pub,
            "agent_pem_pub": agent_pem_pub,
        }
    else:
        return None


def storeAgentECDH(aid, ecdh):
    print("Storing Agent exdh key", "\naid:", aid, "\necdh:", ecdh)
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    cursor = conn.cursor()

    update_query = """
    UPDATE keystore
    SET agent_pem_pub = %s
    WHERE aid = %s;
    """
    values = (ecdh, aid)
    cursor.execute(update_query, values)
    conn.commit()

    cursor.close()
    conn.close()


async def ping(aip, aport):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://{aip}:{aport}/")
        if response.status_code != 200:
            return False
        return True
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
        return False


import httpx


async def transmit(aip, aport, emessage):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://{aip}:{aport}/startupFTPListener/", json=emessage
            )
        if response.status_code != 200:
            return False
        return response.json()
    except httpx.RequestError as exc:
        print(f"An error occurred while posting to agent {exc.request.url!r}: {exc}")
        return False
