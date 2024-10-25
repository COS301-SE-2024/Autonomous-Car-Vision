import os
from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def elyptic(encoding):
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

        return {"private": private_key, "public": public_key}

    return {"private": private_key, "public": public_key}


def encrypt_message(public_key_pem, data):
    try:
        if isinstance(public_key_pem, bytes):
            public_key_pem = public_key_pem.decode("utf-8")

        public_key = serialization.load_pem_public_key(
            public_key_pem.encode("utf-8"), backend=default_backend()
        )
        print("Public key loaded successfully")

        json_data = json.dumps(data)
        print("JSON data to encrypt:", json_data)

        symmetric_key = os.urandom(32)
        iv = os.urandom(16)
        cipher = Cipher(
            algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted_data = (
            encryptor.update(json_data.encode("utf-8")) + encryptor.finalize()
        )

        encrypted_symmetric_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        encrypted_message_base64 = base64.b64encode(encrypted_data).decode("utf-8")
        encrypted_symmetric_key_base64 = base64.b64encode(
            encrypted_symmetric_key
        ).decode("utf-8")
        iv_base64 = base64.b64encode(iv).decode("utf-8")

        print("Encrypted data:", encrypted_message_base64)
        print("Encrypted symmetric key:", encrypted_symmetric_key_base64)
        print("IV:", iv_base64)

        return {
            "encrypted_data": encrypted_message_base64,
            "encrypted_key": encrypted_symmetric_key_base64,
            "iv": iv_base64,
        }

    except Exception as e:
        print("Encryption failed:", str(e))
        raise


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

    print("RSA Private key in PEM format:")
    print(private_pem.decode("utf-8"))
    print("RSA Public key in PEM format:")
    print(public_pem.decode("utf-8"))
    print()
    return {"public": public_pem, "private": private_pem}


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


def decrypt_ecdh_key_with_rsa(rsa_private_key_pem, encrypted_message_base64):
    if isinstance(rsa_private_key_pem, bytes):
        rsa_private_key_pem = rsa_private_key_pem.decode("utf-8")

    rsa_private_key = serialization.load_pem_private_key(
        rsa_private_key_pem.encode("utf-8"), password=None, backend=default_backend()
    )

    encrypted_message = base64.b64decode(encrypted_message_base64)

    decrypted_message = rsa_private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return decrypted_message.decode("utf-8")
