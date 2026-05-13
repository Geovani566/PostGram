import pymysql
import os 
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE'),
        )

connection=get_connection()


with connection.cursor() as cursor:

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100),
        email VARCHAR(100),
        senha VARCHAR(255)
    )
    """)
    print("usuarios criada")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INT AUTO_INCREMENT PRIMARY KEY,
        texto TEXT,
        usuario_id INT,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        cor VARCHAR(7),
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("posts criada")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS likes(
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT,
        post_id INT,
        FOREIGN KEY (post_id) REFERENCES posts(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)
    print("likes criada")

connection.commit()
connection.close()