import unittest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.backends import default_backend
import base64
import os

from cerberus import (
    elyptic,
    encrypt_message,
    asymmetric,
    get_session,
    elyptic_encryptor,
    elyptic_decryptor,
    decrypt_ecdh_key_with_rsa,
)


class TestCryptoFunctions(unittest.TestCase):

    def test_elyptic_key_generation(self):
        keys = elyptic(encoding=True)
        self.assertIn("private", keys)
        self.assertIn("public", keys)
        self.assertIsInstance(keys["private"], ec.EllipticCurvePrivateKey)
        self.assertIsInstance(keys["public"], ec.EllipticCurvePublicKey)

    def test_asymmetric_key_generation(self):
        keys = asymmetric()
        self.assertIn("private", keys)
        self.assertIn("public", keys)
        self.assertTrue(keys["private"].startswith(b"-----BEGIN RSA PRIVATE KEY-----"))
        self.assertTrue(keys["public"].startswith(b"-----BEGIN PUBLIC KEY-----"))

    def test_encrypt_message(self):
        keys = asymmetric()
        public_key_pem = keys["public"]
        data = {"message": "Test message"}

        encrypted_data = encrypt_message(public_key_pem, data)
        self.assertIn("encrypted_data", encrypted_data)
        self.assertIn("encrypted_key", encrypted_data)
        self.assertIn("iv", encrypted_data)

    def test_ecdh_encryption_decryption(self):
        # Generate ECDH keys for two parties
        keys1 = elyptic(encoding=False)
        keys2 = elyptic(encoding=False)

        session_key1 = get_session(keys1["private"], keys2["public"])
        session_key2 = get_session(keys2["private"], keys1["public"])

        plaintext = "This is a secret message"
        encrypted_message = elyptic_encryptor(session_key1, plaintext)
        decrypted_message = elyptic_decryptor(session_key2, encrypted_message)

        self.assertEqual(plaintext, decrypted_message)


if __name__ == "__main__":
    unittest.main()
