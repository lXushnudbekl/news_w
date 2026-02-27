import requests

requests.post(
    "http://192.168.0.149:5000",
    json={
        "phone": "998951010628",
        "text": "Salom Django SMS"
    }
)