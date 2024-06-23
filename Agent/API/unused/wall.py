import pyotp
import os
from dotenv import load_dotenv
import sqlite3
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import otp

load_dotenv()


def simmulate():
    broker = genBroker()
    print("broker otp: ", broker)
    enotp = otp.encrypt_otp(broker, "public_key.pem")
    print("Encrypted otp: ", enotp)
    verified = verify(enotp)
    print("Verified otp status: ", verified)
    return "simmulation successful" if verified else "simmulation failed"


def genBroker():
    secret = os.getenv("SECRET")
    print(secret)
    conn = sqlite3.connect("brokerReg.db")
    cursor = conn.cursor()
    cursor.execute("SELECT counter FROM counter_table WHERE id = 1")
    counter = cursor.fetchone()[0]

    hotp = pyotp.HOTP(secret)
    otp = hotp.at(counter)

    cursor.execute(
        "INSERT INTO audit_table (counter, otp) VALUES (?, ?)", (counter, otp)
    )
    conn.commit()

    new_counter = counter + 1
    cursor.execute("UPDATE counter_table SET counter = ? WHERE id = 1", (new_counter,))
    conn.commit()
    conn.close()

    return otp


def gen():
    secret = os.getenv("SECRET")
    print(secret)

    conn = sqlite3.connect("agentReg.db")
    cursor = conn.cursor()
    cursor.execute("SELECT counter FROM counter_table WHERE id = 1")
    counter = cursor.fetchone()[0]

    hotp = pyotp.HOTP(secret)
    print("counter: ", counter)
    otp = hotp.at(counter)

    cursor.execute(
        "INSERT INTO audit_table (counter, otp) VALUES (?, ?)", (counter, otp)
    )
    conn.commit()

    new_counter = counter + 1
    cursor.execute("UPDATE counter_table SET counter = ? WHERE id = 1", (new_counter,))
    conn.commit()
    conn.close()

    return otp


def verify(encrypted_otp: str):
    decToken = decrypt_otp(encrypted_otp)
    print("decrypted otp: ", decToken)
    verToken = gen()
    print("agent Token: ", verToken)

    if decToken == verToken:
        return {"is_valid": True}
    return {"is_valid": False}


def decrypt_otp(encrypted_otp, private_key_path="private_key.pem"):
    try:
        with open(private_key_path, "rb") as key_file:
            pem_content = key_file.read()
            print(
                "Private key content:\n", pem_content.decode()
            )  # Print the content of the PEM file
            private_key = serialization.load_pem_private_key(pem_content, password=None)

        decrypted_otp = private_key.decrypt(
            encrypted_otp,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return decrypted_otp.decode()
    except Exception as e:
        print("An error occurred:", e)
