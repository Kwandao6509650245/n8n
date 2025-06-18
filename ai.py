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
# data = [
#     {
#         "keywords": [
#             "อัปเดตรหัสล็อกอิน ",
#             "อัปเดตรหัสผ่านใหม่",
#             "อัปเดตรหัสผ่าน",
#             "อัปเดตรหัส",
#             "อัปเดตพาสล็อคอิน",
#             "อัปเดตพาสเข้าระบบ",
#             "อัปเดตชุดล็อกอินใหม่",
#             "อัปเดตคีย์ผ่านเข้า",
#             "อัปเดตข้อมูลเข้าสู่ระบบ",
#             "อัปเดตโค้ดล็อกอินใหม่",
#             "อัปเกรดรหัสเข้าใช้",
#             "อยากเปลี่ยนพาสเวิด",
#             "สร้างล็อคอินใหม่",
#             "สร้างระบบล็อคอินใหม่",
#             "สร้างระบบคีย์ใหม่",
#             "สร้างรหัสปลอดภัยใหม่",
#             "สร้างรหัสใหม่",
#             "สร้างพาสโค้ดใหม่",
#             "สร้างพาสเวิร์ดใหม่",
#             "สร้างโค้ดล็อกอินใหม่",
#             "รีเฟรชระบบเข้าสู่ระบบ",
#             "รีเฟรชรหัสผ่าน",
#             "รีเฟรชคีย์ล็อกอินใหม่",
#             "รีเฟรชข้อมูลรหัส",
#             "รีเฟรชการล็อกอิน",
#             "รีเซ็ตระบบปลอดภัย",
#             "รีเซ็ตรหัสรักษาความปลอดภัย",
#             "รีเซ็ตรหัสผ่าน"
#         ],
#         "response": "คุณครูสามารถเปลี่ยนรหัสผ่านด้วยตนเอง โดยทำตามขั้นตอนดังนี้:\n1. เข้าสู่ระบบ ด้วยบัญชีผู้ใช้งานปัจจุบัน\n2. ไปที่เมนู บัญชี > เปลี่ยนรหัสผ่าน\n3. กรอกข้อมูลดังนี้:\n  - รหัสผ่านเดิม\n  - รหัสผ่านใหม่\n  - ยืนยันรหัสผ่านใหม่\n4. กดปุ่ม 'บันทึก' เพื่อยืนยันการเปลี่ยนรหัสผ่าน\n5. ระบบจะแจ้งว่าเปลี่ยนรหัสผ่านสำเร็จ"
#     }
# ]

data = [
    {
    "keywords": [
        "รบกวนอัปเดตอีเมลในโปรไฟล์ของฉันด้วยครับ/ค่ะ",
        "รบกวนช่วยแก้ไขที่อยู่อีเมลของฉันด้วยครับ/ค่ะ",
        "รบกวนแก้ไขที่อยู่อีเมลในโปรไฟล์ของฉันให้เป็นปัจจุบัน",
        "รบกวนแก้ไขข้อมูลอีเมลที่ลงทะเบียนไว้ในระบบ",
        "รบกวนแก้ไขข้อมูลอีเมลที่ลงทะเบียนให้เป็นปัจจุบันด้วย",
        "รบกวนแก้ไขข้อมูลอีเมลให้ถูกต้องด้วยครับ/ค่ะ",
        "รบกวนแก้ไขข้อมูลอีเมลเพื่อให้เป็นข้อมูลล่าสุด",
        "รบกวนเปลี่ยนที่อยู่อีเมลให้ถูกต้องตามนี้ครับ/ค่ะ",
        "ต้องการแก้ไขข้อมูลอีเมลที่ผูกกับบัญชีนี้",
        "ต้องการแก้ไขข้อมูลอีเมลที่ใช้ในระบบ กรุณาช่วยดำเนินการด้วยครับ/ค่ะ",
        "ต้องการเปลี่ยนอีเมลสำหรับติดต่อเป็นอีเมลนี้ครับ/ค่ะ",
        "ต้องการเปลี่ยนอีเมลติดต่อให้เป็นอีเมลนี้",
        "ต้องการเปลี่ยนอีเมลในระบบเป็น [อีเมลใหม่]",
        "ต้องการเปลี่ยนแปลงอีเมลที่ใช้งานในบัญชี",
        "ช่วยอัปเดตอีเมลของฉันเป็นอีเมลใหม่ด้วยครับ/ค่ะ",
        "ช่วยอัปเดตอีเมลใหม่ให้ในระบบด้วยครับ/ค่ะ",
        "ช่วยอัปเดตอีเมลในบัญชีของฉันด้วยครับ/ค่ะ",
        "ช่วยอัปเดตที่อยู่อีเมลในระบบให้ตรงกับอีเมลใหม่ครับ/ค่ะ",
        "ช่วยแก้ไขอีเมลในระบบให้ตรงกับข้อมูลล่าสุดด้วยครับ/ค่ะ",
        "ช่วยแก้ไขที่อยู่อีเมลในระบบเป็นอีเมลใหม่ให้ด้วยครับ/ค่ะ",
        "ช่วยแก้ไขข้อมูลอีเมลของฉันให้เป็นอีเมลใหม่ตามที่แจ้งด้วยครับ/ค่ะ",
        "ช่วยเปลี่ยนอีเมลที่อยู่ในระบบเป็นอีเมลใหม่ให้ด้วยครับ/ค่ะ",
        "ช่วยเปลี่ยนอีเมลในระบบเป็นอีเมลนี้แทน",
        "ฉันพบว่าข้อมูลอีเมลผิดพลาด รบกวนแก้ไขให้ด้วยครับ/ค่ะ",
        "ฉันต้องการเปลี่ยนแปลงอีเมลในบัญชีผู้ใช้",
        "ขออัปเดตอีเมลใหม่ในระบบแทนอีเมลเก่า",
        "ขอความอนุเคราะห์แก้ไขอีเมลที่ผิดพลาดในระบบ",
        "ขอความร่วมมือแก้ไขอีเมลในบัญชีผู้ใช้",
        "ขอความกรุณาอัปเดตอีเมลในโปรไฟล์ให้ถูกต้อง",
        "ขอความกรุณาแก้ไขอีเมลในระบบให้ถูกต้องด้วยครับ/ค่ะ",
        "ขอให้แก้ไขอีเมลเดิมเป็นอีเมลใหม่ดังนี้ครับ/ค่ะ",
        "ขอโทษที่รบกวนครับ/ค่ะ ขอแก้ไขที่อยู่อีเมลให้ด้วย",
        "ขอแก้ไขอีเมลที่ลงทะเบียนไว้เป็นอีเมลใหม่ครับ/ค่ะ",
        "ขอแก้ไขอีเมลที่ใช้ในการติดต่อให้เป็นอีเมลใหม่",
        "ขอเปลี่ยนอีเมลในระบบเป็นอีเมลนี้แทนครับ/ค่ะ",
        "กรุณาตรวจสอบและแก้ไขที่อยู่อีเมลให้ถูกต้องด้วยครับ/ค่ะ",
        "กรุณาช่วยแก้ไขที่อยู่อีเมลตามข้อมูลใหม่ให้ด้วยครับ/ค่ะ",
        "กรุณาแก้ไขอีเมลในระบบให้เป็นอีเมลใหม่ด้วยครับ/ค่ะ",
        "กรุณาเปลี่ยนอีเมลที่ใช้ติดต่อเป็นอีเมลใหม่ให้ด้วย",
        "กรุณาเปลี่ยนอีเมลในระบบตามข้อมูลใหม่ด้วยครับ/ค่ะ"
    ],
    "response": "คุณครูสามารถแก้ไขอีเมลได้ด้วยตนเองค่ะ ทำตามขั้นตอนดังนี้\n1. ล็อกอินเข้าระบบ แล้วมาที่เมนู บัญชี ดังรูป จากนั้นระบบจะแสดงหน้าข้อมูลส่วนตัวค่ะ\n2. ทำการแก้ไขข้อมูลอีเมลให้ตรงกับระบบ ENDB จากนั้นกดบันทึก ปุ่มด้านล่างค่ะ และกดปิดหน้าข้อมูลส่วนตัว\n3. เมื่อแก้ไขอีเมลเรียบร้อยแล้ว คุณครูสามารถเข้าระบบ ENDB ด้วยอีเมลเดิมได้เลยค่ะ\nสอบถามเพิ่มเติมได้ที่ teacherpd@ipst.ac.th พร้อมแจ้งหมายเลขอ้างอิง 52006 เพื่อใช้อ้างอิงและติดตามงานค่ะ"
}
]

import requests
import json

# Define the API endpoint
url = "http://localhost:11434/api/embed"

# Define the payload (data to send in the request body)


# --- Process and Store ---
# for item in data:
#     keywords_list = item["keywords"]
#     response_text = item["response"]
#     for keyword in keywords_list:
#         content = "Question: " + keyword + "Answer: " + response_text
#         payload = {
#         "model": "mxbai-embed-large",
#         "input": content
#         }
#         # print(payload)
#         response = requests.post(url, json=payload)
#         # print(response)
#         # Raise an HTTPError for bad responses (4xx or 5xx)
#         response.raise_for_status()
#         embedding_data = response.json()
#         print(embedding_data['embeddings'][0])
#         cur.execute("INSERT INTO documents (content, embedding) VALUES (%s, %s)", (content, embedding_data['embeddings'][0]))
#         conn.commit()


content = "ขอแก้ไขอีเมล"
payload = {
        "model": "mxbai-embed-large",
        "input": content
        }
        # print(payload)
response = requests.post(url, json=payload)
embedding_data = response.json()
print(embedding_data['embeddings'][0])
# print(embedding_data)

limit=5
cur.execute("""
SELECT content, embedding <-> %s AS distance
FROM documents
ORDER BY distance
LIMIT %s
    """, (embedding_data['embeddings'][0], limit))
result = cur.fetchall()

print(f"Search results for: '{result}'")
for i, (content, distance) in enumerate(result, 1):
    print(f"{i}. {content} (Distance: {distance:.4f})")


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
