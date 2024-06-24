def aegis():
    print("<========== Starting AEGIS protocol ==========>")

    print(">>> Generating RSA key")
    init = asymmetric()
    server_priv = init["private"]
    server_pub = init["public"]

    server_public_pem = server_pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    print(">>> Server public key")
    print(server_public_pem.decode("utf-8"))

    print(">>> Generating ECDH key")
    agentInit = elyptic()
    agent_private = agentInit["private"]
    agent_public = agentInit["public"]

    print(">>> Encrypting agent public key for transmission")
    encrypted_agent_public_key = server_pub.encrypt(
        agent_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    print("\nEncrypted agent public key:", encrypted_agent_public_key)

    print(">>> Received and decrypted agent public key")
    received_agent_public_key_pem = server_priv.decrypt(
        encrypted_agent_public_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    print("\nReceived agent public key PEM:", received_agent_public_key_pem)

    print("\n>>> Loading agent public key from PEM format")
    agent_public_key = serialization.load_pem_public_key(
        received_agent_public_key_pem, backend=default_backend()
    )
    print(agent_public_key)

    print("\nGenerating server's ECDH key pair")
    server_key_pair = generate_elliptic_key_pair()
    server_key_priv = server_key_pair["private"]
    server_key_public = server_key_pair["public"]

    print(">>> Encrypting server public key using a shared secret")
    shared_secret = agent_private.exchange(ec.ECDH(), agent_public_key)

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"handshake data",
        backend=default_backend(),
    ).derive(shared_secret)

    server_public_bytes = server_key_public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    iv = os.urandom(16)
    cipher = Cipher(
        algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend()
    )
    encryptor = cipher.encryptor()
    encrypted_server_ecdh_public_key = (
        encryptor.update(server_public_bytes) + encryptor.finalize()
    )
    print("\nEncrypted server ECDH public key:", encrypted_server_ecdh_public_key)

    print(">>> Received and decrypted server's public key")
    cipher = Cipher(
        algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend()
    )
    decryptor = cipher.decryptor()
    received_server_ecdh_public_key_pem = (
        decryptor.update(encrypted_server_ecdh_public_key) + decryptor.finalize()
    )
    print("\nReceived server ECDH public key PEM:", received_server_ecdh_public_key_pem)

    server_ecdh_public_key = serialization.load_pem_public_key(
        received_server_ecdh_public_key_pem, backend=default_backend()
    )

    print(">>> Deriving shared secret")
    agent_shared_secret = agent_private.exchange(ec.ECDH(), server_ecdh_public_key)
    server_shared_secret = server_key_priv.exchange(ec.ECDH(), agent_public_key)

    derived_key_agent = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"handshake data",
        backend=default_backend(),
    ).derive(agent_shared_secret)

    derived_key_server = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"handshake data",
        backend=default_backend(),
    ).derive(server_shared_secret)

    # Verify that both derived keys are the same
    assert derived_key_agent == derived_key_server

    print("Shared secret derived successfully and both keys match.")

    print("<========== End Protocol ==========>")
    return 0
