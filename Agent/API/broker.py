from fastapi import FastAPI, BackgroundTasks, Request
import requests
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()

HOST_IP = os.getenv("HOST_IP")

app = FastAPI()

def checkVerified():
    return True

# For now, GET
@app.get("/getAgentData/")
def getAgentIp():
    if(checkVerified()):
        url = "http://" + HOST_IP + ":8001/startup/"
        print("Sending request to: ", url)  
        response = requests.get(url)
        
        print("Response Body: ", response.json())
        print("Response Status: ", response.status_code)
        return {"status": response.json()}
    else:
        return {"status": "Not Verified"}
        

@app.post("/register/")
async def register(request: Request):
    data = await request.json()
    print(f"Received registration data: {data}")
    return {"status": "Received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)