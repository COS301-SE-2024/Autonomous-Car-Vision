from fastapi import FastAPI, BackgroundTasks, Request
import requests
import uvicorn

app = FastAPI()

def checkVerified():
    # Here we would check the database for the verification status
    return True

# For now, GET
@app.get("/getAgentData/")
def getAgentIp():
    # Here we would use a database lookup to get the IP 
    # Then get the port from a request
    if(checkVerified()):
        url = "http://127.0.0.1:8001/startup/"
        print("Sending request to: ", url)  
        response = requests.get(url)
        
        print("Response Body: ", response.json())
        print("Response Status: ", response.status_code)
        return {"status": response.json()}
    else:
        return {"status": "Not Verified"}
        

@app.post("/register/")
async def register(request: Request):
    # Here we would add the data to the database and await it to be verified
    data = await request.json()
    print(f"Received registration data: {data}")
    return {"status": "Received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)