import requests
import json
import psycopg2
from sqlalchemy import create_engine, Column, Integer, Text, JSON
# from sqlalchemy.o import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.dialects.postgresql import VECTOR  # Requires pgvector and extension created
from pgvector.sqlalchemy import Vector

# --- Database config ---
DATABASE_URL = 'postgresql://myuser:mypassword@localhost:5432/mydatabase'


# --- SQLAlchemy Setup ---
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS documents (
#         id SERIAL PRIMARY KEY,
#         content TEXT,
#         embedding vector(1536)
#     )
# """)
# conn.commit()
# print("Connection to the database successful!")

# # --- Data ---
data = [
    {
        "keywords": [
            "อัปเดตรหัสล็อกอิน ",
            "อัปเดตรหัสผ่านใหม่",
            "อัปเดตรหัสผ่าน",
            "อัปเดตรหัส",
            "อัปเดตพาสล็อคอิน",
            "อัปเดตพาสเข้าระบบ",
            "อัปเดตชุดล็อกอินใหม่",
            "อัปเดตคีย์ผ่านเข้า",
            "อัปเดตข้อมูลเข้าสู่ระบบ",
            "อัปเดตโค้ดล็อกอินใหม่",
            "อัปเกรดรหัสเข้าใช้",
            "อยากเปลี่ยนพาสเวิด",
            "สร้างล็อคอินใหม่",
            "สร้างระบบล็อคอินใหม่",
            "สร้างระบบคีย์ใหม่",
            "สร้างรหัสปลอดภัยใหม่",
            "สร้างรหัสใหม่",
            "สร้างพาสโค้ดใหม่",
            "สร้างพาสเวิร์ดใหม่",
            "สร้างโค้ดล็อกอินใหม่",
            "รีเฟรชระบบเข้าสู่ระบบ",
            "รีเฟรชรหัสผ่าน",
            "รีเฟรชคีย์ล็อกอินใหม่",
            "รีเฟรชข้อมูลรหัส",
            "รีเฟรชการล็อกอิน",
            "รีเซ็ตระบบปลอดภัย",
            "รีเซ็ตรหัสรักษาความปลอดภัย",
            "รีเซ็ตรหัสผ่าน"
        ],
        "response": "คุณครูสามารถเปลี่ยนรหัสผ่านด้วยตนเอง โดยทำตามขั้นตอนดังนี้:\n1. เข้าสู่ระบบ ด้วยบัญชีผู้ใช้งานปัจจุบัน\n2. ไปที่เมนู บัญชี > เปลี่ยนรหัสผ่าน\n3. กรอกข้อมูลดังนี้:\n  - รหัสผ่านเดิม\n  - รหัสผ่านใหม่\n  - ยืนยันรหัสผ่านใหม่\n4. กดปุ่ม 'บันทึก' เพื่อยืนยันการเปลี่ยนรหัสผ่าน\n5. ระบบจะแจ้งว่าเปลี่ยนรหัสผ่านสำเร็จ"
    }
]

import requests
import json

# Define the API endpoint
url = "http://localhost:11434/api/embed"

# Define the payload (data to send in the request body)


# --- Process and Store ---
for item in data:
    keywords_list = item["keywords"]
    response_text = item["response"]
    for keyword in keywords_list:
        content = "Question: " + keyword + "Answer: " + response_text
        payload = {
        "model": "mxbai-embed-large",
        "input": content
        }
        # print(payload)
        response = requests.post(url, json=payload)
        # print(response)
        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        embedding_data = response.json()
        print(embedding_data['embeddings'][0])
        cur.execute("INSERT INTO documents (content, embedding) VALUES (%s, %s)", (content, embedding_data['embeddings'][0]))
        conn.commit()





    # print(payload)


#     record = KeywordEmbedding(
#         keywords=item['keywords'],
#         response=item['response'],
#         embedding=embedding
#     )
#     session.add(record)

# session.commit()
# session.close()

print("✅ Data stored with local embedding via Ollama.")
