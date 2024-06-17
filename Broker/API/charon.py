import os
import psycopg2
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

def asymmetric():
    print(">>> Asymmetric key generation in progress")

    server_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    server_public_key = server_private_key.public_key()

    private_pem = server_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = server_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    print("Private key in PEM format:")
    print(private_pem.decode('utf-8'))
    print("Public key in PEM format:")
    print(public_pem.decode('utf-8'))
    print()
    return {'public': public_pem, 'private': private_pem}


def obol():
    init_key_pair = asymmetric()
    load_dotenv()

    dbname = os.getenv('POSTGRES_DB')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')

    print(f"Connecting to database {dbname} at {host}:{port} with user {user}")

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO keystore (init_key, initkey_validation)
    VALUES (%s, %s)
    RETURNING aid;
    """
    values = (init_key_pair['private'].decode('utf-8'), False)
    cursor.execute(insert_query, values)
    aid = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()
    return {'aid': aid, 'public': init_key_pair['public']}


def asymmetric_decryption(aid, message):
    load_dotenv()

    dbname = os.getenv('POSTGRES_DB')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')

    print(f"Connecting to database {dbname} at {host}:{port} with user {user}")

    try:
        with psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
        ) as conn:
            with conn.cursor() as cursor:
                select_query = """
                SELECT init_key FROM keystore
                WHERE aid = %s;
                """
                cursor.execute(select_query, (aid,))
                priv_key = cursor.fetchone()[0]

                # priv_key is already in string format, no need to decode
                print("Private key in PEM format:")
                print(priv_key)
                private_key = serialization.load_pem_private_key(priv_key.encode(), password=None, backend=default_backend())

                # Decode the Base64 encoded message
                decoded_message = base64.b64decode(message)

                decrypted_message = private_key.decrypt(
                    decoded_message,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                print("Decrypted message:", decrypted_message.decode('utf-8'))
                return {'aid': aid, 'private': priv_key}

    except Exception as e:
        print(f"An error occurred: {e}")
        return None