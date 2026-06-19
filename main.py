from fastapi import  FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
app = FastAPI()
load_dotenv()
templates = Jinja2Templates(directory="templates")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
class Question(BaseModel):
    question: str
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
@app.get("/status")
def status():
    return {"status":"active"}
@app.get("/name")
def name():
    return {"name":"Career Assist"}
@app.get("/message")
def message():
    response = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": "Give a short career advice for a computer science student."}])
    return {"response": response.choices[0].message.content}
@app.post("/ask")
def ask_ai(data: Question):
    response = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": data.question}])
    return {"answer": response.choices[0].message.content}

