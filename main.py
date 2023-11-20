from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from typing import Annotated

class Chat(BaseModel):
    id: int
    content: str

chats = []

app = FastAPI()

@app.post('/items')
def create_item(image: UploadFile, 
                title: Annotated[str,Form()], 
                price: Annotated[int, Form()], 
                description: Annotated[str, Form()], 
                place: Annotated[str, Form()]):
    print(image, title, price, description, place)
    return '200'

@app.get("/chat")
def read_chat():
    return chats

@app.post("/chat")
def create_memo(chat: Chat):
    chats.append(chat)
    return '채팅 추가에 성공했습니다.'




app.mount('/', StaticFiles(directory="frontend", html=True), name="frontend")



