# import requests
# import time
# import concurrent.futures

# def send_request_hvstat():
#     url = "http://206.189.188.197:8000/hvstat/"
#     # data = {"uid": "1234567890"}
#     response = requests.get(url)
#     # return response.json()

# def send_request_verifyOTP():
#     url = "http://206.189.188.197:8000/verifyOTP/"
#     data = {"uid": "1234567890", "otp": "123456"}
#     response = requests.post(url, data=data)
#     # return response.json()

# def send_request_otpRegenerate():
#     url = "http://206.189.188.197:8000/otpRegenerate/"
#     data = {"uid": "1234567890", "uemail": "test@test.com"}
#     response = requests.post(url, data=data)
#     # return response.json()

# def send_request_getAgentUserConnections():
#     url = "http://206.189.188.197:8000/getAgentUserConnections/"
#     data = {"uid": "1"}
#     response = requests.post(url, data=data)
#     # return response.json()

# def send_request_getSalt():
#     url = "http://206.189.188.197:8000/getSalt/"
#     data = {"uemail": "test@test.com"}
#     response = requests.post(url, data=data)
#     # return response.json()

# def send_request_signin():
#     url = "http://206.189.188.197:8000/signin/"
#     data = {"uid": "1", "password": "password", "uemail": "dev@gmail.com"}
#     response = requests.post(url, data=data)
#     # return response.json()

# def send_request_signout():
#     url = "http://206.189.188.197:8000/signout/"
#     data = {"uid": "1"}
#     response = requests.post(url, data=data)
#     # return response.json()

# def send_request_devLogin():
#     url = "http://206.189.188.197:8000/devLogin/"
#     data = {"uid": "1", "password": "password", "uemail": "dev@gmail.com"}
#     response = requests.post(url, data=data)
#     # return response.json()
    
# def send_request_findOpenPort():
#     url = "http://206.189.188.197:8010/findOpenPort/"
#     response = requests.get(url)
#     # return response.json()
    
# def send_request_test():
#     url = "http://206.189.188.197:8006/test/"
#     data = {"message": "hello"}
#     response = requests.post(url, data=data)
#     # return response.json()
    
# def send_request_simStore():
#     url = "http://206.189.188.197:8010/simStore/"
#     response = requests.post(url)
#     # return response.json()

# def send_request_getUserData():
#     url = "http://206.189.188.197:8000/getUserData/"
#     data = {"uid": "1"}
#     response = requests.post(url, data=data)
#     # return response.json()

# def run_stress_test(num_requests, functions):
#     for i in functions:
#         start_time = time.time()
#         with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
#             futures = [executor.submit(i) for _ in range(num_requests)]
#             results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
#         end_time = time.time()
#         print("Average time taken for ", i.__name__, ": ", (end_time - start_time)/num_requests)       


# if __name__ == "__main__":
#     num_requests = 30
#     start_time = time.time()
#     functions = [send_request_hvstat, send_request_verifyOTP, send_request_otpRegenerate, send_request_getAgentUserConnections, send_request_getSalt, send_request_signin, send_request_signout, send_request_devLogin, send_request_findOpenPort, send_request_test, send_request_simStore, send_request_getUserData]
    
#     print("Testing ")
    
    # results = run_stress_test(num_requests, functions)
    
    # end_time = time.time()
    # print(f"Time taken: {end_time - start_time:.2f} seconds")
    # print(f"Total requests: {num_requests * len(functions)}")
    # print(f"Requests per second: {(num_requests * len(functions)) / (end_time - start_time):.2f}")
    # print(f"Number of functions: {len(functions)}")

    
import json
from datetime import datetime
import requests

def get_uptime():
    url = "https://api.uptimerobot.com/v2/getMonitors"
    
    payload = "api_key=m797755729-8a15e04da92d199157c69016"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }
    
    response = requests.request("POST", url, data=payload, headers=headers)
    data = response.json()
    
    if data['stat'] == 'ok':
        monitors = data['monitors']
        for monitor in monitors:
            name = monitor['friendly_name']
            uptime_ratio = monitor['all_time_uptime_ratio']
            status = monitor['status']
            
            print(f"Monitor: {name}")
            print(f"Uptime: {uptime_ratio}%")
            print(f"Status: {'Up' if status == 2 else 'Down'}")
            print("---")
    else:
        print("Failed to retrieve monitor data")

if __name__ == "__main__":
    get_uptime()
