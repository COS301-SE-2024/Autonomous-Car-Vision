# for broker use
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization


def encrypt_otp(otp, public_key_path="public_key.pem"):
    try:
        with open(public_key_path, "rb") as key_file:
            pem_content = key_file.read()
            print(
                "Public key content:\n", pem_content.decode()
            )  # Print the content of the PEM file
            public_key = serialization.load_pem_public_key(pem_content)

        encrypted_otp = public_key.encrypt(
            otp.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return encrypted_otp
    except Exception as e:
        print("An error occurred:", e)
