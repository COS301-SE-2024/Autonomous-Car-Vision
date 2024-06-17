from fastapi import FastAPI, HTTPException
import httpx
# import keygen
# import setup
# import wall
import cerberus

app = FastAPI()


# @app.on_event("startup")
# async def startup_event():
#     setup.setup_database()
#     setup.setup_database_broker()
#

@app.get("/")
def status():
    return {"status": "online"}


@app.get("/install")
async def install():
    async with httpx.AsyncClient() as client:
        # get my agent details
        # TODO abstract away. This gets replaced by byundling into the msi setup...
        response = await client.get('http://127.0.0.1:8006/agent')
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching external data")
        print("Response:", response.json())
        # encrypt my public ecd key


        init_elyptic = cerberus.elyptic(True)
        agent_public = init_elyptic['public']
        agent_private = init_elyptic['private']


        # TODO persist the keys in pem files



        encrypted_message = cerberus.encrypt_message(response.json()['public'], agent_public)
        print("Encrypted message: ", encrypted_message)
        # transmit my ecd key
        response2 = await client.post('http://127.0.0.1:8006/test',
                                      json={"aid": response.json()['aid'], "message": encrypted_message})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching external data")

        return response.json()
