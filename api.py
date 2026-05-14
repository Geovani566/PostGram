from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
import pymysql
import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        port=int(os.getenv('MYSQL_PORT')),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

@app.get("/testar_db")
async def testar_db():

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            resultado = cursor.fetchone()

        conn.close()

        return {
            "status": "banco conectado",
            "resultado": resultado
        }

    except Exception as e:
        return {
            "erro_mysql": str(e)
        }


@app.get("/")
def home():
    return{
        "status":"api online"
    }


@app.post("/login")
async def login(request : Request):
    dados=await request.json()
    email=dados["email"]
    senha=dados["senha"]
    conn = get_connection()

    
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE  email= %s AND senha =%s",(email,senha))
        usuario = cursor.fetchone()
        
        if usuario :
            conn.close()
            return {
                "status":"login efetuado com sucesso!",
                "usuario_id":usuario[0],
                "nome": usuario[1] 
            }
        else:
            conn.close()
            return {
                "status":"usuario não encontrado!"
            }
    
        
@app.post("/cadastrar")
async def cadastrar(request: Request):
    dados= await request.json()
    nome=dados['nome']
    email=dados["email"]
    senha=dados["senha"]
    
    conn =get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM usuarios WHERE email=%s",(email,))
        if cursor.fetchone() :
            cursor.close()
            return {
                "status":"Email já cadastrado!"
            }
        cursor.execute("INSERT INTO usuarios (nome,email,senha) VALUES(%s,%s,%s)",(nome,email,senha))
        conn.commit()
        conn.close()
        return {"status":"Conta criada com sucesso!"}




@app.post("/posts")
async def posts(request: Request):
    dados = await request.json()
    post = dados['post']
    if len(post)==0:
        return {"status": "Post vazio!"}
    if len(post)>200:
        return {"status": "Máximo 200 caracteres!"}
    usuario_id = dados['usuario_id']
    cor = dados['cor']

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO posts (texto, usuario_id, cor) VALUES(%s, %s, %s)", (post, usuario_id, cor))
        conn.commit()
        conn.close()
    return {"status": "Post criado!"}





@app.get('/ver_posts')
async def ver_posts():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT posts.id, posts.texto, usuarios.nome, posts.cor, posts.data_criacao 
            FROM posts 
            JOIN usuarios ON posts.usuario_id = usuarios.id
        """)
        posts = cursor.fetchall()
        
    conn.close()
    return {"posts": [{"id":p[0],"texto": p[1], "nome": p[2], "cor": p[3],"data_criacao": p[4].strftime("%d/%m/%Y") if p[4] else ""} for p in posts]}






@app.get('/meus_posts/{usuario_id}')
async def meus_posts(usuario_id:int):
    conn=get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
        SELECT posts.id ,posts.texto,posts.cor,posts.data_criacao
        FROM posts WHERE posts.usuario_id = %s
""",(usuario_id,))
        posts=cursor.fetchall()
    conn.close()
    lista=[]
    for p in posts:
        lista.append({
            "id":p[0],
            "texto":p[1],
            "cor":p[2],
            "data_criacao":p[3].strftime("%d/%m/%Y") if p[3] else ""})
    return  {"posts":lista}
        
@app.delete("/deletar_posts/{post_id}")
async def deletar_posts(post_id:int ,request:Request):
    dados = await request.json()
    usuario_id = dados['usuario_id']

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM posts WHERE id = %s AND usuario_id = %s", (post_id, usuario_id))
        conn.commit()
        deletados = cursor.rowcount
    conn.close()

    if deletados == 0:
        return {"status": "Post não encontrado ou sem permissão!"}
    return {"status": "Post deletado!"}

@app.post('/like/{post_id}')
async def like(post_id:int,request:Request):
    dados=await request.json()
    usuario_id=dados['usuario_id']
    conn = get_connection()

    with conn.cursor() as cursor :
        cursor.execute("SELECT * FROM likes WHERE usuario_id=%s AND post_id=%s",(usuario_id,post_id))
        like=cursor.fetchone()
        if like:
            cursor.execute("DELETE FROM likes WHERE usuario_id=%s AND post_id=%s",(usuario_id,post_id))
            conn.commit()
            conn.close()
            return {
                "status":"like retirado!"
            }
       


        cursor.execute("INSERT INTO likes (usuario_id,post_id) VALUES (%s,%s)",(usuario_id,post_id))
        
        conn.commit()
    conn.close()
    return {"status":"like dado!"}
