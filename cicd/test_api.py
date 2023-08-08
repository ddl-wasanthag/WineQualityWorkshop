#requires the model API access token
import requests
import json

url = "https://wgamage18435.cs.domino.tech:443/models/64d1255bca137a66a4a4a2ce/latest/model"
payload = {
    "data": {
        "density": 0.99,
        "volatile_acidity": 0.028,
        "chlorides": 0.05,
        "is_red": 0,
        "alcohol": 11
    }
}

response = requests.post(url,
    auth=(
        "<DOMINO_MODEL_API_ACCESS_TOKEN>",
        "<DOMINO_MODEL_API_ACCESS_TOKEN>"
    ),
    json={
    "data": {
        "density": 0.99,
        "volatile_acidity": 0.028,
        "chlorides": 0.05,
        "is_red": 0,
        "alcohol": 11
    }
}
)


if response.status_code == 200:
    json_response = response.json()
    prediction = json_response['result']['prediction']
    print(prediction)
else:
    print("Error:", response.status_code)
    print("Response content:", response.content)


