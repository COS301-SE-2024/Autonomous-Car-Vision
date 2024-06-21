from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from fastapi import FastAPI, HTTPException
import httpx
import cerberus

app = FastAPI()


@app.get("/")
def status():
    return {"status": "online"}


@app.get("/install")
async def install():
    async with httpx.AsyncClient() as client:
        # get my agent details
        response = await client.get('http://127.0.0.1:8006/agent')
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching external data")
        print("Response:", response.json())

        # encrypt my public ecd key
        init_elyptic = cerberus.elyptic(True)
        agent_public = init_elyptic['public']
        agent_private = init_elyptic['private']

        agent_rsa = cerberus.asymmetric()
        agent_rsa_public = agent_rsa['public']
        agent_rsa_private = agent_rsa['private']

        data_to_encrypt = {
            "aid": response.json()['aid'],
            "ecd_key": agent_public.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8'),
            "rsa_key": agent_rsa_public.decode('utf-8')
        }
        print("JSON data for encryption:", data_to_encrypt)

        encrypted_message = cerberus.encrypt_message(response.json()['public'], data_to_encrypt)
        print("Encrypted message: ", encrypted_message)

        # Transmit the encrypted data
        response2 = await client.post('http://127.0.0.1:8006/test',
                                      json={"aid": response.json()['aid'], "message": encrypted_message})
        if response2.status_code != 200:
            raise HTTPException(status_code=response2.status_code, detail="Error posting encrypted data")
        print("Response:", response2.json())
        # session = cerberus.get_session(agent_private,)
        server_ecdh = cerberus.decrypt_ecdh_key_with_rsa(agent_rsa_private, response2.json()['encrypted_ecdh'])
        print("server ecdh decoded", server_ecdh)
        server_ecdh2 = load_pem_public_key(server_ecdh.encode('utf-8'))
        session = cerberus.get_session(agent_private, server_ecdh2)
        message = cerberus.elyptic_encryptor(session, "hello")
        response3 = await client.post('http://127.0.0.1:8006/message',
                                      json={"aid": response.json()['aid'], "message": message})
        if response3.status_code != 200:
            raise HTTPException(status_code=response2.status_code, detail="Error posting encrypted data")
        print("Response:", response3.json())
        print(server_ecdh)
        return {'message': "success"}
