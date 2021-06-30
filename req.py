import requests

url = "http://127.0.0.1:8000/ap/v1/alarm/1/ack/"

headers = {
    "Content-Type": "application/json",
}

response = requests.post(url=url, headers=headers)
print(response.status_code)
print(response.json())
