from fastapi import FastAPI, HTTPException, Query, Request
from datetime import datetime
from dateutil import parser
from slugify import slugify
from faker import Faker
import hashlib, uuid, re, pytz, qrcode, base64, io, math, random
from pydantic import BaseModel
import barcode
from barcode.writer import ImageWriter
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.extension import _rate_limit_exceeded_handler

# python -m uvicorn UPAPI:app --reload

app = FastAPI(title="UPAPI")
fake = Faker()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def limit_body(request: Request, call_next):
    content_length = request.headers.get("content-length")

    if content_length and int(content_length) > 1024 * 1024:
        raise HTTPException(413, "Payload too big")

    return await call_next(request)

@app.get("/hash")
@limiter.limit("5/minute")
def generate_hash(request: Request, algo: str = "sha256", text: str=""):
    try:
        h = hashlib.new(algo)
        h.update(text.encode())
        return {"hash": h.hexdigest()}
    except:
        raise HTTPException(400, "Invalid hash algorithm")

@app.get("/uuid")
@limiter.limit("5/minute")
def generate_uuid(request: Request, ):
    return {"uuid": str(uuid.uuid4())}

@app.get("/text/upper")
@limiter.limit("5/minute")
def text_upper(request: Request, text: str):
    return {"text": str(text.upper())}

@app.get("/text/lower")
@limiter.limit("5/minute")
def text_lower(request: Request, text: str):
    return {"text": str(text.lower())}

@app.get("/text/count")
@limiter.limit("5/minute")
def text_count(request: Request, text: str):
    return {"text": len(text)}

@app.get("/date/now")
@limiter.limit("5/minute")
def date_now(request: Request, timezone: str = "UTC"):
    timez = pytz.timezone(timezone)
    return {"date": str(datetime.now(timez).isoformat())}

@app.get("/date/difference")
@limiter.limit("5/minute")
def date_difference(request: Request, date1: str, date2: str):
    a = parser.parse(date1)
    b = parser.parse(date2)

    return {"seconds": abs((b - a).total_seconds())}

@app.get("/math/ruleof3")
@limiter.limit("5/minute")
def ruleof3(request: Request, a: float, b: float, c: float):
    return {"result": (b*c) / a}

@app.get("/math/randint")
@limiter.limit("5/minute")
def randominteger(request: Request, minimum: int, maximum: int):
    if minimum > maximum:
        raise HTTPException(400, "minimum cannot be greater than maximum")
    return {"result": random.randint(minimum, maximum)}

@app.get("/fakeuser")
@limiter.limit("5/minute")
def fakeuser(request: Request, ):
    return {"username": fake.user_name(), "name": fake.name(), "birthday": fake.date_of_birth(), "address": fake.address(), "email": fake.email()}

@app.get("/fakecreditcard")
@limiter.limit("5/minute")
def fakecreditcard(request: Request, ):
    return {"name": fake.name(), "number": fake.credit_card_number(), "provider": fake.credit_card_provider(), "expiredate": fake.credit_card_expire(), "code": fake.credit_card_security_code()}

@app.get("/generatepassword")
@limiter.limit("5/minute")
def genpassword(request: Request, ):
    password = fake.password()
    return {"password": password}

@app.get("/qrcode")
@limiter.limit("5/minute")
def qr(request: Request, text: str):
    img = qrcode.make(text)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode()
    return {"image": base64_img}

class Barcode(BaseModel):
    text: str
    
@app.post("/barcode")
@limiter.limit("5/minute")
def genbarcode(request: Request, data: Barcode):
    buffer = io.BytesIO()
    code128 = barcode.get("code128", data.text, writer=ImageWriter())
    code128.write(buffer)
    base64_img = base64.b64encode(buffer.getvalue()).decode()

    return {"image": base64_img}

@app.get("/geodist")
@limiter.limit("5/minute")
def geodist(request: Request, lat1:float, lon1:float, lat2:float, lon2:float):
    R = 6371
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2 #haversine
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) # Transforma aquele valor angular na distância sobre a esfera.
    return {"km": R * c} # Multiplica a distancia pelo raio

# Encripting
class Encript(BaseModel):
    key: str
    text: str

@app.post("/encript")
@limiter.limit("5/minute")
def encript_data(request: Request, encripted: Encript):
    text_bytes = encripted.text.encode("utf-8")
    key_bytes = encripted.key.encode("utf-8")

    result = bytearray()

    for i in range(len(text_bytes)):
        result.append(text_bytes[i] ^ key_bytes[i % len(key_bytes)])

    return base64.urlsafe_b64encode(result).decode("utf-8")

@app.post("/decript")
@limiter.limit("5/minute")
def decript_data(request: Request, decript: Encript):
    data = base64.urlsafe_b64decode(decript.text)
    key_bytes = decript.key.encode("utf-8")

    result = bytearray()

    for i in range(len(data)):
        result.append(data[i] ^ key_bytes[i % len(key_bytes)])

    return result.decode("utf-8")