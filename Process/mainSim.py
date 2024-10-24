import requests
from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv

load_dotenv()

HOST_IP = os.getenv("HOST_IP")
print(HOST_IP)  

def regAgent(num):
    try:
        response = requests.get("http://" + HOST_IP + ":8006/simAgent")
        response.raise_for_status()
        reg1 = {
            "aid": response.json()["aid"],
            "aip": HOST_IP,
            "aport": 8010 if num == 1 else 8011,
            "capacity": "dual",
            "storage": 290.4,
            "identifier": "ACDC",
        }
        print(response)
        response2 = requests.post("http://" + HOST_IP + ":8006/simHandshake", json=reg1)
        response2.raise_for_status()
        print(response2)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return None


# print(regAgent(1).text)
# print(regAgent(2).text)

def findAgentSim():
    response = requests.post("http://" + HOST_IP + ":8006/simStore")
    response.raise_for_status()
    print(response.text)
findAgentSim()