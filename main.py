from fastapi import FastAPI, UploadFile, Form, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

#DB 연결
conn = sqlite3.connect('database.db', check_same_thread=False)
#
cur = conn.cursor()


class Chat(BaseModel):
    id: int
    content: str

chats = []

app = FastAPI()

@app.post('/items')
async def create_item(image: UploadFile, 
                title: Annotated[str,Form()], 
                price: Annotated[int, Form()], 
                description: Annotated[str, Form()], 
                place: Annotated[str, Form()],
                insertAt: Annotated[int, Form()]):
    #이미지 데이터는 블록타입이라서 크게 오기 때문에 데이터를 읽을 시간이 필요함
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO 
                items(title, image, price, description, place, insertAt)
                VALUES('{title}','{image_bytes.hex()}','{price}','{description}','{place}','{insertAt}')
                """)
    conn.commit()
    return '200'

@app.get('/items')
async def get_items():
    #컬럼명을 같이 불러오는 코드
    conn.row_factory = sqlite3.Row
    #다음 행동을 진행하기 위한 cursor 이동
    cur = conn.cursor()
    rows = cur.execute(f"""
                       SELECT * FROM items
                       """).fetchall()
    #JSONResponse(dict(rows)) 그냥 진행하게 되면
    #해당 데이터는 어떤 컬럼의 데이터인지를 모르기 때문에 에러가 발생
    #rows = [['id', 1], ['title','~~~~'], ['',''], ['','']]
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))

@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = conn.cursor()
    #현재 16진법
    image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id={item_id}
                              """).fetchone()[0]
    
    return Response(content=bytes.fromhex(image_bytes))


@app.get("/chat")
def read_chat():
    return chats

@app.post("/chat")
def create_memo(chat: Chat):
    chats.append(chat)
    return '채팅 추가에 성공했습니다.'




app.mount('/', StaticFiles(directory="frontend", html=True), name="frontend")



