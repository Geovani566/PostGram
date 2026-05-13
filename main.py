import pymysql

connection = pymysql.connect(
    host='localhost',
    user='usuario',
    password='senha',
    database='base_de_dados',
)

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