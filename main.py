from fastapi import FastAPI, UploadFile, Form, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
import sqlite3

#DB 연결
conn = sqlite3.connect('database.db', check_same_thread=False)
#
cur = conn.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items(
	            id INTEGER PRIMARY KEY,
	            title TEXT NOT NULL,
	            image BLOB,
	            price INTEGER NOT NULL,
	            description TEXT,
	            place TEXT NOT NULL,
	            insertAt INTEGER NOT NULL
            );
            """)

class Chat(BaseModel):
    id: int
    content: str

chats = []

app = FastAPI()

SERCRET = "super-coding"
manager = LoginManager(SERCRET, '/login')

@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data['id']}"'''
        #컬럼명을 같이 불러오는 코드
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    user = cur.execute(f"""
                       SELECT * FROM users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

@app.post('/login')
def login(id:Annotated[str, Form()], 
          password: Annotated[str, Form()]):
    user = query_user(id)
    if not user:
        #자동으로 401 error발생하게 해준다.
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(data={
        'sub': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
        }
    })
    
    return {'access_token': access_token}

@app.post("/signup")
def signup(id:Annotated[str, Form()], password:Annotated[str, Form()],
           name: Annotated[str, Form()],
           email: Annotated[str, Form()]):
    
    cur.execute(f"""
                INSERT INTO users(id, name, email, password)
                VALUES ('{id}','{name}','{email}','{password}')
                """)
    conn.commit()
    
    return '200'

@app.post('/items')
async def create_item(image: UploadFile, 
                title: Annotated[str,Form()], 
                price: Annotated[int, Form()], 
                description: Annotated[str, Form()], 
                place: Annotated[str, Form()],
                insertAt: Annotated[int, Form()],
                user=Depends(manager)):
    # 이미지 데이터는 블록타입이라서 크게 오기 때문에 데이터를 읽을 시간이 필요함
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO 
                items(title, image, price, description, place, insertAt)
                VALUES('{title}','{image_bytes.hex()}','{price}','{description}','{place}','{insertAt}')
                """)
    conn.commit()
    return '200'

@app.get('/items')
async def get_items(user=Depends(manager)):
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
    
    #media_type의 경우 배포 버전에 따라서 명시적으로 해줘야하고 안해주고 차이가 존재
    #deta-space의 경우 python3.9까지 적용중이라고 함(현재 나의 버전 3.12)
    return Response(content=bytes.fromhex(image_bytes), media_type="image/*")




@app.get("/chat")
def read_chat():
    return chats

@app.post("/chat")
def create_memo(chat: Chat):
    chats.append(chat)
    return '채팅 추가에 성공했습니다.'




app.mount('/', StaticFiles(directory="frontend", html=True), name="frontend")



