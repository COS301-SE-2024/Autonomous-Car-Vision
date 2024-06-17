from fastapi import FastAPI, Request
# import setup
import charon

app = FastAPI()


# @app.on_event("startup")
# async def startup_event():
#     setup.setup_database()
#     setup.setup_database_broker()


@app.get("/")
def status():
    return {"status": "online"}


@app.get("/agent")
def agent():
    response = charon.obol()

    # first it should generate a key.

    # insert key into a key store
    # then it should package that key into an msi file.
    # and return the agent

    return response

# @app.post("/register")
# async def register(request: Request):


@app.post("/test")
async def test(request: Request):
    message = await request.json()
    mresp = charon.asymmetric_decryption(message['aid'],message['message'])
    return mresp



# @app.post("/areg")
# def areg():
# @app.get("/sim")
# def simulate():
#     print("simulate")
#     return wall.simmulate()
#
#
# @app.get("/crypt")
# def crypt():
#     return keygen.generate_keys()
