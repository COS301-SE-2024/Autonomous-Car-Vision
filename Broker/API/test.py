import pytest
from unittest.mock import patch, MagicMock
from cryptography.hazmat.primitives.asymmetric import ec
from unittest.mock import patch, MagicMock
from charon import (
    asymmetric,
    elyptic,
    get_session,
    elyptic_encryptor,
    elyptic_decryptor,
)


@pytest.fixture
def mock_db_connection():
    with patch("psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        yield mock_conn


def test_asymmetric():
    result = asymmetric()
    assert "public" in result
    assert "private" in result
    assert isinstance(result["public"], bytes)
    assert isinstance(result["private"], bytes)


def test_elyptic():
    result = elyptic(True)
    assert "private" in result
    assert "public" in result
    assert isinstance(result["private"], ec.EllipticCurvePrivateKey)
    assert isinstance(result["public"], ec.EllipticCurvePublicKey)


def test_get_session():
    private_key = ec.generate_private_key(ec.SECP256R1())
    peer_public_key = ec.generate_private_key(ec.SECP256R1()).public_key()

    session_key = get_session(private_key, peer_public_key)
    assert isinstance(session_key, bytes)
    assert len(session_key) == 32


def test_elyptic_encryption_decryption():
    session_key = b"0" * 32
    plaintext = "Hello, World!"
    encrypted = elyptic_encryptor(session_key, plaintext)
    decrypted = elyptic_decryptor(session_key, encrypted)
    assert decrypted == plaintext


def test_elyptic_encryption_decryption_false():
    session_key = b"0" * 32
    plaintext = "Hello, World!"
    encrypted = elyptic_encryptor(session_key, plaintext)
    encrypted.upper()
    decrypted = elyptic_decryptor(session_key, encrypted)
    assert decrypted is not "Hello, World!"


def test_elyptic_encryption_decryption_false_key():
    session_key = b"0" * 32
    plaintext = "Hello, World!"
    encrypted = elyptic_encryptor(session_key, plaintext)
    decrypted = elyptic_decryptor(session_key.upper(), encrypted)
    assert decrypted is not "Hello, World!"


@pytest.fixture
def mock_db_connection():
    with patch("psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        yield mock_conn


def test_obol(mock_db_connection):
    from charon import obol

    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchone.return_value = [1]  # Mocking the returned aid
    result = obol()
    assert "aid" in result
    assert "public" in result
    assert result["aid"] == 1
    mock_cursor.execute.assert_called_once()
    call_args = mock_cursor.execute.call_args[0]
    assert "INSERT INTO keystore" in call_args[0]
    mock_db_connection.commit.assert_called_once()


def test_store_agent_keys(mock_db_connection):
    from charon import store_agent_keys

    aid = 1
    ecdh_pub = b"mock_ecdh_public_key"
    rsa_pub = b"mock_rsa_public_key"
    store_agent_keys(aid, ecdh_pub, rsa_pub)
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.execute.assert_called_once()
    call_args = mock_cursor.execute.call_args[0]
    assert "UPDATE keystore" in call_args[0]
    assert call_args[1][0] == ecdh_pub.decode("utf-8")
    assert call_args[1][1] == aid
    mock_db_connection.commit.assert_called_once()


def test_store_agent_keys_false(mock_db_connection):
    from charon import store_agent_keys
    aid = 1
    ecdh_pub = b"mock_ecdh_public_key"
    rsa_pub = b"mock_rsa_public_key"
    store_agent_keys(aid, ecdh_pub, rsa_pub)
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.execute.assert_called_once()
    call_args = mock_cursor.execute.call_args[0]
    assert "UPDATE keystore" in call_args[0]
    assert call_args[1][0] == ecdh_pub.decode("utf-8")
    assert call_args[1][1] is not 2
    mock_db_connection.commit.assert_called_once()


def checking_encoding_works(mock_db_connection):
    from charon import store_agent_keys

    aid = 1
    ecdh_pub = b"mock_ecdh_public_key"
    rsa_pub = b"mock_rsa_public_key"
    store_agent_keys(aid, ecdh_pub, rsa_pub)
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.execute.assert_called_once()
    call_args = mock_cursor.execute.call_args[0]
    assert "UPDATE keystore" in call_args[0]
    assert call_args[1][0] is not ecdh_pub.decode("utf-7")
    assert call_args[1][1] is not 2
    mock_db_connection.commit.assert_called_once()