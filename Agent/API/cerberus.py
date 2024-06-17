from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding
import base64
import os


def aegis():
    print("<========== Starting AEGIS protocol ==========>")

    print(">>> Generating RSA key")
    init = asymmetric()
    server_priv = init['private']
    server_pub = init['public']

    server_public_pem = server_pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    print(">>> Server public key")
    print(server_public_pem.decode('utf-8'))

    print(">>> Generating ECDH key")
    agentInit = elyptic()
    agent_private = agentInit['private']
    agent_public = agentInit['public']

    print(">>> Encrypting agent public key for transmission")
    encrypted_agent_public_key = server_pub.encrypt(
        agent_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print('\nEncrypted agent public key:', encrypted_agent_public_key)

    print(">>> Received and decrypted agent public key")
    received_agent_public_key_pem = server_priv.decrypt(
        encrypted_agent_public_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print('\nReceived agent public key PEM:', received_agent_public_key_pem)

    print("\n>>> Loading agent public key from PEM format")
    agent_public_key = serialization.load_pem_public_key(
        received_agent_public_key_pem,
        backend=default_backend()
    )
    print(agent_public_key)

    print("\nGenerating server's ECDH key pair")
    server_key_pair = generate_elliptic_key_pair()
    server_key_priv = server_key_pair['private']
    server_key_public = server_key_pair['public']

    print(">>> Encrypting server public key using a shared secret")
    shared_secret = agent_private.exchange(ec.ECDH(), agent_public_key)

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(shared_secret)

    server_public_bytes = server_key_public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_server_ecdh_public_key = encryptor.update(server_public_bytes) + encryptor.finalize()
    print('\nEncrypted server ECDH public key:', encrypted_server_ecdh_public_key)

    print(">>> Received and decrypted server's public key")
    cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    received_server_ecdh_public_key_pem = decryptor.update(encrypted_server_ecdh_public_key) + decryptor.finalize()
    print('\nReceived server ECDH public key PEM:', received_server_ecdh_public_key_pem)

    server_ecdh_public_key = serialization.load_pem_public_key(
        received_server_ecdh_public_key_pem,
        backend=default_backend()
    )

    print(">>> Deriving shared secret")
    agent_shared_secret = agent_private.exchange(ec.ECDH(), server_ecdh_public_key)
    server_shared_secret = server_key_priv.exchange(ec.ECDH(), agent_public_key)

    derived_key_agent = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(agent_shared_secret)

    derived_key_server = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(server_shared_secret)

    # Verify that both derived keys are the same
    assert derived_key_agent == derived_key_server

    print("Shared secret derived successfully and both keys match.")

    print("<========== End Protocol ==========>")
    return 0


def elyptic(encoding):
    print(">>> Generating ECDH key pair")
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    if encoding:
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        print(">>> Elyptic keys encoded to pem format")
        print("Private Key:")
        print(private_pem.decode('utf-8'))

        print("Public Key:")
        print(public_pem.decode('utf-8'))

        return {'private': private_key, 'public': public_key}

    print(">>> Elyptic keys not encoded to pem format")
    print("Private Key:")
    print(private_key)

    print("Public Key:")
    print(public_key)

    return {'private': private_key, 'public': public_key}


def asymmetric():
    print(">>> Asymmetric key generation in progress")
    server_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    server_public_key = server_private_key.public_key()
    print("Private key")
    print(server_private_key)
    print("Public key")
    print(server_public_key)
    return {'public': server_public_key, 'private': server_private_key}


# aegis()

def encrypt_message(public_key_pem, message):

    # Takes in a pem format (non serialized) ecdh key
    public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'), backend=default_backend())
    ecdh_public_key_pem = message.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    encrypted_message = public_key.encrypt(
        ecdh_public_key_pem,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # Encode the encrypted message using Base64
    encrypted_message_base64 = base64.b64encode(encrypted_message).decode('utf-8')
    return encrypted_message_base64