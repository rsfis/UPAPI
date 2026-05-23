from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from dateutil import parser
from slugify import slugify
from faker import Faker
import hashlib, uuid, re, pytz, qrcode, base64, io, math, random

# python -m uvicorn UPAPI:app --reload

app = FastAPI(title="UPAPI")
fake = Faker()

@app.get("/hash")
def generate_hash(algo: str = "sha256", text: str=""):
    try:
        h = hashlib.new(algo)
        h.update(text.encode())
        return {"hash": h.hexdigest()}
    except:
        raise HTTPException(400, "Invalid hash algorithm")

@app.get("/uuid")
def generate_uuid():
    return {"uuid": str(uuid.uuid4())}

@app.get("/text/upper")
def text_upper(text: str):
    return {"text": str(text.upper())}

@app.get("/text/lower")
def text_lower(text: str):
    return {"text": str(text.lower())}

@app.get("/text/count")
def text_count(text: str):
    return {"text": str(text.count())}

@app.get("/date/now")
def date_now(timezone: str = "UTC"):
    timez = pytz.timezone(timezone)
    return {"date": str(datetime.now(timez).isoformat())}

@app.get("/date/difference")
def date_difference(date1: str, date2: str):
    a = parser.parse(date1)
    b = parser.parse(date2)

    return {"seconds": abs((b - a).total_seconds())}

@app.get("/math/ruleof3")
def ruleof3(a: float, b: float, c: float):
    return {"result": (b*c) / a}

@app.get("/math/randint")
def randominteger(minimum: int, maximum: int):
    return {"result": random.randint(minimum, maximum)}

@app.get("/fakeuser")
def fakeuser():
    return {"username": fake.user_name(), "name": fake.name(), "birthday": fake.date_of_birth(), "address": fake.address(), "email": fake.email()}

@app.get("/fakecreditcard")
def fakecreditcard():
    return {"name": fake.name(), "number": fake.credit_card_number(), "provider": fake.credit_card_provider(), "expiredate": fake.credit_card_expire(), "code": fake.credit_card_security_code()}

@app.get("/qrcode")
def qr(text: str):
    img = qrcode.make(text)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode()
    return {"image": base64_img}

@app.get("/geodist")
def geodist(lat1:float, lon1:float, lat2:float, lon2:float):
    R = 6371
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2 #haversine
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) # Transforma aquele valor angular na distância sobre a esfera.
    return {"km": R * c} # Multiplica a distancia pelo raio