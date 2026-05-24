# UPAPI
Universal Purpose API
https://upapi-production.up.railway.app

UPAPI is a Universal Purpose API, made for facilitating boring programming tasks.

# Docs
## GET /hash
Returns the HASH of a text.
Params: algo: str = "sha256", text: str=""
Returns: {"hash"}

## GET /uuid
Returns a random UUID
Params: N/A
Returns: {"uuid"}

## GET /text/upper
Returns a text upper cased
Params: text: str=""
Returns: {"text"}

## GET /text/lower
Returns a text lower cased
Params: text: str=""
Returns: {"text"}

## GET /text/count
Returns the quantity of chars from a text
Params: algo: text: str=""
Returns: {"text"}

## GET /date/now
Returns today date in isoformat
Params: N/A
Returns: {"date"}

## GET /date/difference
Returns the difference between 2 dates in seconds
Params: date1: str, date2: str -> Dates must be in isoformat!
Returns: {"seconds"}

## GET /math/ruleof3
Returns the fourth number of a rule of 3 equation
Params: float a, float b, float c
Returns: {"result"}

## GET /math/randint
Returns a random integer
Params: int minimum, int maximum
Returns: {"result"}

## GET /fakeuser
Returns a random fake user
Params: N/A
Returns: {"username", "name", "birthday", "address", "email"}

## GET /fakecreditcard
Returns a random fake credit card
Params: N/A
Returns: {"name", "number", "provider", "expiredate", "code"}

## GET /generatepassword
Returns a random strong password of 10 digit
Params: N/A
Returns: {"password"}

## GET /qrcode
Returns a base64 encoded png of a QRCode
Params: text: str
Returns: {"image"}

## POST /barcode
Returns a base64 encoded png of a Barcode
Params: text: str
Returns: {"image"}

## GET /geodist
Returns the distance between 2 points (latitude and longitude) in KM on the Earth
Params: lat1:float, lon1:float, lat2:float, lon2:float
Returns: {"km"}

## POST /encript
Returns a encrypted code that can be only decripted using the secret key defined by the user
Params: text: str, key: str
Returns: {"result"}

## POST /decript
Returns the decripted text using the secret key defined by the user
Params: text: str, key: str
Returns: {"result"}

# How to use using python
```
import requests
import base64

"""
#QR_CODE

base64_string =requests.get("https://upapi-production.up.railway.app/qrcode", params={"text": "Hello world"}).json()["image"]

with open("qrcode.png", "wb") as f:
    f.write(base64.b64decode(base64_string))
"""

"""
#BARCODE

base64_string = requests.post(
    "https://upapi-production.up.railway.app/barcode",
    json={"text": "BomDia"}
).json()["image"]

with open("barcode.png", "wb") as f:
    f.write(base64.b64decode(base64_string))
"""


"""
#Encript

data = {
    "text": "I love my daddy",
    "key": "examplekey"
}

resposta = requests.post("https://upapi-production.up.railway.app/encript", json=data)
print(resposta.json())
"""

"""
#Decript
data = {
    "text": "LwxNAwYeRxwfTxEGBVUMEVULEhYH",
    "key": "examplekey"
}

resposta = requests.post("https://upapi-production.up.railway.app/decript", json=data)
print(resposta.json())
"""
```
