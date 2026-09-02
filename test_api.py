import requests

url = "http://127.0.0.1:8000/api/predict/"

data = {
    "age": 22,
    "weight": 50,
    "height": 165,
    "bmi": 18.37,
    "cycle": 0,
    "cycle_length": 28,
    "weight_gain": 0,
    "hair_growth": 0,
    "pimples": 0
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())