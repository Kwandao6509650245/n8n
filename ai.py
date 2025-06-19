import requests
import json
import psycopg2
from sqlalchemy import create_engine, Column, Integer, Text, JSON
# from sqlalchemy.o import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.dialects.postgresql import VECTOR  # Requires pgvector and extension created
from pgvector.sqlalchemy import Vector

import ollama
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document
import pandas as pd


# --- Database config ---
DATABASE_URL = 'postgresql://myuser:mypassword@localhost:5432/mydatabase'

DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mydatabase"
CONNECTION_STRING = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
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


# data = [
#     {
#         "keywords": [
#             "ตั้งรหัสผ่านยังไง",
#             "ขอตั้งรหัสผ่านครั้งแรก",
#             "เริ่มใช้งานต้องตั้งรหัสตรงไหน",
#             "อยากตั้งพาสเวิร์ดใหม่",
#             "เริ่มต้นใช้งานต้องตั้งรหัสยังไง",
#             "ระบบให้ตั้งรหัสผ่านยังไงบ้าง",
#             "ต้องตั้งรหัสยังไงก่อนเข้าใช้",
#             "สมัครใช้งานแล้วต้องตั้งรหัสไหม",
#             "พึ่งเริ่มใช้ ต้องตั้งพาสเวิร์ดยังไง",
#             "ขั้นตอนการตั้งรหัสมีอะไรบ้าง",
#             "ขอลิงก์ตั้งรหัสผ่านหน่อย",
#             "ตั้งรหัสล็อกอินครั้งแรกทำยังไง",
#             "เริ่มต้นระบบต้องตั้งคีย์ยังไง",
#             "สมัครแล้วแต่ยังไม่ได้ตั้งรหัส",
#             "ลืมตั้งรหัสตอนสมัคร ต้องทำยังไง"
#         ],
#         "response": "คุณครูสามารถตั้งรหัสผ่านครั้งแรกได้ตามขั้นตอนดังนี้:\n1. ไปที่หน้าเข้าสู่ระบบของระบบครูผู้สอน\n2. คลิกที่ปุ่ม 'ตั้งรหัสผ่านครั้งแรก' หรือ 'ลืมรหัสผ่าน'\n3. กรอกอีเมลที่ใช้ลงทะเบียน\n4. ระบบจะส่งลิงก์สำหรับตั้งรหัสผ่านไปยังอีเมลของคุณ\n5. เปิดอีเมลแล้วคลิกลิงก์ดังกล่าว\n6. ตั้งรหัสผ่านใหม่และยืนยันรหัสอีกครั้ง\n7. กด 'บันทึก' เพื่อใช้งานรหัสผ่านใหม่ในการเข้าสู่ระบบ"
#     }
# ]


data = [
    {
        "keywords" : [
            "อยากตั้งรหัสผ่านใหม่ต้องทำยังไง",
            "ต้องเริ่มตั้งรหัสผ่านจากตรงไหน",
            "ขอวิธีตั้งรหัสผ่านสำหรับใช้งานครั้งแรก",
            "ยังไม่เคยตั้งรหัส ต้องเริ่มที่ไหน",
            "ระบบให้ตั้งรหัสผ่านยังไง",
            "รบกวนแนะนำขั้นตอนการตั้งพาสเวิร์ด",
            "สมัครแล้ว ยังไม่ตั้งรหัสผ่านเลย",
            "ต้องใช้ลิงก์ไหนในการตั้งรหัส",
            "ตั้งรหัสล็อกอินครั้งแรกต้องทำยังไงบ้าง",
            "ยังไม่เคยตั้งรหัส ขอวิธีหน่อย",
            "อยากสร้างรหัสผ่านใหม่ ขอคำแนะนำ",
            "ต้องตั้งรหัสผ่านเองใช่ไหม",
            "ตั้งรหัสผ่านต้องใช้อะไรบ้าง",
            "มีขั้นตอนยังไงในการตั้งพาสเวิร์ด",
            "ขอตัวอย่างวิธีตั้งรหัสผ่าน",
            "ลิงก์สำหรับตั้งรหัสผ่านคืออันไหน",
            "ยังไม่มีรหัสผ่านเลย ต้องทำยังไง",
            "ตั้งค่ารหัสครั้งแรกตรงไหน",
            "สมัครแล้วต้องตั้งรหัสยังไงต่อ",
            "ช่วยแนะนำวิธีตั้งรหัสผ่านทีครับ",
            "พึ่งลงทะเบียน ต้องตั้งรหัสไหม",
            "ตั้งพาสเวิร์ดยังไงถึงจะปลอดภัย",
            "มีคำแนะนำการตั้งรหัสไหม",
            "วิธีสร้างพาสเวิร์ดเริ่มต้นคืออะไร",
            "ถ้าเพิ่งสมัคร ต้องตั้งรหัสยังไง",
            "ต้องตั้งรหัสผ่านผ่านหน้าเว็บไหน",
            "ยังไม่มีพาสเวิร์ด ขอวิธีตั้ง",
            "สมัครใช้งานแล้ว ต้องสร้างรหัสยังไง",
            "ต้องคลิกลิงก์ไหนเพื่อตั้งพาส",
            "อยากได้ขั้นตอนสร้างรหัสผ่าน",
            "ขอคำแนะนำตั้งรหัสผ่านปลอดภัย",
            "พึ่งลงทะเบียน ต้องกำหนดรหัสตรงไหน",
            "ยังไม่ได้ตั้งรหัส ขอขั้นตอน",
            "ขอวิธีตั้งพาสล็อกอินทีครับ",
            "ขอตัวช่วยในการตั้งรหัสผ่าน",
            "ต้องเข้าเมนูไหนเพื่อสร้างรหัส",
            "ตั้งรหัสผ่านใหม่ครั้งแรกทำยังไง",
            "เริ่มใช้งานระบบต้องทำยังไงกับพาสเวิร์ด",
            "ต้องตั้งรหัสยาวแค่ไหน",
            "มีข้อกำหนดในการตั้งพาสเวิร์ดไหม",
            "สมัครแล้วระบบให้ตั้งรหัสตอนไหน",
            "มีแบบฟอร์มสำหรับตั้งรหัสไหม",
            "ต้องสร้างพาสเองใช่ไหม",
            "ต้องใช้รหัสอะไรตอนแรก",
            "มีอีเมลตั้งรหัสส่งมาหรือยัง",
            "จะเริ่มใช้ ต้องมีรหัสก่อนใช่ไหม",
            "สร้างรหัสผ่านต้องยืนยันด้วยไหม",
            "ต้องใส่รหัสอะไรตอนเริ่ม",
            "ต้องคลิกลิงก์ไหนในอีเมล",
            "ขอตัวอย่างรหัสที่ปลอดภัย",
            "ยังไม่เคยล็อกอินเลย ต้องทำอะไร",
            "ตั้งรหัสในแอปหรือหน้าเว็บ",
            "ระบบจะส่งลิงก์ตั้งรหัสมาใช่ไหม",
            "ขอลิงก์สำหรับกำหนดพาสใหม่",
            "ขอตั้งพาสสำหรับเข้าสู่ระบบ",
            "ตั้งรหัสผ่านใหม่ตอนเริ่มต้นได้ไหม",
            "สร้างพาสใหม่ในระบบยังไง",
            "อยากสร้างพาสให้ปลอดภัย ต้องทำยังไง",
            "มีวิธีแนะนำตั้งรหัสให้ปลอดภัยไหม",
            "รหัสผ่านต้องมีตัวพิเศษไหม",
            "ตั้งรหัสผ่านต้องใช้ภาษาอังกฤษไหม",
            "มีเงื่อนไขอะไรในการตั้งรหัสบ้าง",
            "เริ่มตั้งรหัสต้องมีอะไรบ้าง",
            "ตั้งรหัสเสร็จแล้วจะเข้าได้เลยไหม",
            "ระบบส่งลิงก์มาตั้งรหัสหรือเปล่า",
            "ตั้งรหัสผ่านผ่านมือถือได้ไหม",
            "จะเปลี่ยนจากไม่มีรหัสเป็นมีรหัสยังไง",
            "อยากเปิดใช้งานบัญชี ต้องทำยังไงกับรหัส",
            "ตั้งรหัสตอนแรกต้องยืนยันทางไหน",
            "ระบบจะให้ตั้งรหัสตอนล็อกอินเลยไหม",
            "การตั้งรหัสต้องใช้เวลานานไหม",
            "สมัครแล้วแต่ยังเข้าไม่ได้ ต้องตั้งพาสก่อนใช่ไหม",
            "การตั้งรหัสผ่านต้องมีเงื่อนไขอะไรบ้าง",
            "ตั้งรหัสผ่านให้เด็กนักเรียนต้องทำยังไง",
            "รหัสผ่านแรกเข้าใช้งานต้องกำหนดเองไหม",
            "ต้องใช้รหัสที่ระบบกำหนดหรือเราตั้งเอง",
            "ยังไม่สามารถเข้าใช้งานได้ เพราะยังไม่ได้ตั้งรหัส",
            "ระบบแจ้งให้ตั้งรหัสตอนเข้าใช้งานครั้งแรก",
            "จะตั้งรหัสผ่านครั้งแรกได้จากตรงไหน",
            "ต้องใช้รหัสที่ได้รับจากอีเมลก่อนตั้งใหม่ไหม",
            "ตั้งรหัสผ่านสำหรับบัญชีครูทำยังไง",
            "มีคู่มือการตั้งรหัสผ่านไหม",
            "ขอตัวอย่างการตั้งรหัสผ่านดีๆ หน่อย",
            "เริ่มใช้ระบบครั้งแรก ต้องตั้งพาสก่อนหรือเปล่า",
            "พอสมัครแล้ว จะตั้งรหัสผ่านจากตรงไหน",
            "ต้องรออนุมัติก่อนถึงจะตั้งรหัสได้ไหม",
            "ต้องตั้งรหัสทันทีหลังสมัครหรือเปล่า",
            "สามารถตั้งรหัสผ่านใหม่ผ่านอีเมลได้ไหม",
            "สมัครผ่านแล้วต้องทำอะไรต่อกับรหัส",
            "รหัสเริ่มต้นต้องตั้งเองหรือระบบกำหนดให้",
            "ยังไม่ได้ตั้งรหัส ขอความช่วยเหลือ",
            "อยากใช้งานระบบ ต้องเริ่มที่รหัสผ่านก่อนใช่ไหม",
            "ต้องคลิกลิงก์ในอีเมลเพื่อตั้งรหัสไหม",
            "มีข้อความเตือนให้ตั้งรหัสใหม่ ต้องทำยังไง",
            "เริ่มต้นตั้งรหัสผ่านใหม่จากตรงไหน",
            "ยังไม่สามารถล็อกอินได้ เพราะยังไม่ได้ตั้งพาส",
            "ตั้งรหัสผ่านครั้งแรกต้องผ่านการยืนยันอะไรไหม",
            "ขอรายละเอียดการตั้งรหัสผ่านทีครับ",
            "เริ่มเข้าใช้งานระบบยังไม่ได้เพราะไม่มีรหัส",
            "ต้องคลิก 'ลืมรหัสผ่าน' เพื่อเริ่มตั้งใหม่ไหม"
    ]
    ,
    "response": "คุณครูสามารถตั้งรหัสผ่านครั้งแรกได้ตามขั้นตอนดังนี้:\n1. ไปที่หน้าเข้าสู่ระบบของระบบครูผู้สอน\n2. คลิกที่ปุ่ม 'ตั้งรหัสผ่านครั้งแรก' หรือ 'ลืมรหัสผ่าน'\n3. กรอกอีเมลที่ใช้ลงทะเบียน\n4. ระบบจะส่งลิงก์สำหรับตั้งรหัสผ่านไปยังอีเมลของคุณ\n5. เปิดอีเมลแล้วคลิกลิงก์ดังกล่าว\n6. ตั้งรหัสผ่านใหม่และยืนยันรหัสอีกครั้ง\n7. กด 'บันทึก' เพื่อใช้งานรหัสผ่านใหม่ในการเข้าสู่ระบบ"
    }
]

# data = [
#     {
#     "keywords": [
#         "รบกวนอัปเดตอีเมลในโปรไฟล์ของฉันด้วยครับ/ค่ะ",
#         "รบกวนช่วยแก้ไขที่อยู่อีเมลของฉันด้วยครับ/ค่ะ",
#         "รบกวนแก้ไขที่อยู่อีเมลในโปรไฟล์ของฉันให้เป็นปัจจุบัน",
#         "รบกวนแก้ไขข้อมูลอีเมลที่ลงทะเบียนไว้ในระบบ",
#         "รบกวนแก้ไขข้อมูลอีเมลที่ลงทะเบียนให้เป็นปัจจุบันด้วย",
#         "รบกวนแก้ไขข้อมูลอีเมลให้ถูกต้องด้วยครับ/ค่ะ",
#         "รบกวนแก้ไขข้อมูลอีเมลเพื่อให้เป็นข้อมูลล่าสุด",
#         "รบกวนเปลี่ยนที่อยู่อีเมลให้ถูกต้องตามนี้ครับ/ค่ะ",
#         "ต้องการแก้ไขข้อมูลอีเมลที่ผูกกับบัญชีนี้",
#         "ต้องการแก้ไขข้อมูลอีเมลที่ใช้ในระบบ กรุณาช่วยดำเนินการด้วยครับ/ค่ะ",
#         "ต้องการเปลี่ยนอีเมลสำหรับติดต่อเป็นอีเมลนี้ครับ/ค่ะ",
#         "ต้องการเปลี่ยนอีเมลติดต่อให้เป็นอีเมลนี้",
#         "ต้องการเปลี่ยนอีเมลในระบบเป็น [อีเมลใหม่]",
#         "ต้องการเปลี่ยนแปลงอีเมลที่ใช้งานในบัญชี",
#         "ช่วยอัปเดตอีเมลของฉันเป็นอีเมลใหม่ด้วยครับ/ค่ะ",
#         "ช่วยอัปเดตอีเมลใหม่ให้ในระบบด้วยครับ/ค่ะ",
#         "ช่วยอัปเดตอีเมลในบัญชีของฉันด้วยครับ/ค่ะ",
#         "ช่วยอัปเดตที่อยู่อีเมลในระบบให้ตรงกับอีเมลใหม่ครับ/ค่ะ",
#         "ช่วยแก้ไขอีเมลในระบบให้ตรงกับข้อมูลล่าสุดด้วยครับ/ค่ะ",
#         "ช่วยแก้ไขที่อยู่อีเมลในระบบเป็นอีเมลใหม่ให้ด้วยครับ/ค่ะ",
#         "ช่วยแก้ไขข้อมูลอีเมลของฉันให้เป็นอีเมลใหม่ตามที่แจ้งด้วยครับ/ค่ะ",
#         "ช่วยเปลี่ยนอีเมลที่อยู่ในระบบเป็นอีเมลใหม่ให้ด้วยครับ/ค่ะ",
#         "ช่วยเปลี่ยนอีเมลในระบบเป็นอีเมลนี้แทน",
#         "ฉันพบว่าข้อมูลอีเมลผิดพลาด รบกวนแก้ไขให้ด้วยครับ/ค่ะ",
#         "ฉันต้องการเปลี่ยนแปลงอีเมลในบัญชีผู้ใช้",
#         "ขออัปเดตอีเมลใหม่ในระบบแทนอีเมลเก่า",
#         "ขอความอนุเคราะห์แก้ไขอีเมลที่ผิดพลาดในระบบ",
#         "ขอความร่วมมือแก้ไขอีเมลในบัญชีผู้ใช้",
#         "ขอความกรุณาอัปเดตอีเมลในโปรไฟล์ให้ถูกต้อง",
#         "ขอความกรุณาแก้ไขอีเมลในระบบให้ถูกต้องด้วยครับ/ค่ะ",
#         "ขอให้แก้ไขอีเมลเดิมเป็นอีเมลใหม่ดังนี้ครับ/ค่ะ",
#         "ขอโทษที่รบกวนครับ/ค่ะ ขอแก้ไขที่อยู่อีเมลให้ด้วย",
#         "ขอแก้ไขอีเมลที่ลงทะเบียนไว้เป็นอีเมลใหม่ครับ/ค่ะ",
#         "ขอแก้ไขอีเมลที่ใช้ในการติดต่อให้เป็นอีเมลใหม่",
#         "ขอเปลี่ยนอีเมลในระบบเป็นอีเมลนี้แทนครับ/ค่ะ",
#         "กรุณาตรวจสอบและแก้ไขที่อยู่อีเมลให้ถูกต้องด้วยครับ/ค่ะ",
#         "กรุณาช่วยแก้ไขที่อยู่อีเมลตามข้อมูลใหม่ให้ด้วยครับ/ค่ะ",
#         "กรุณาแก้ไขอีเมลในระบบให้เป็นอีเมลใหม่ด้วยครับ/ค่ะ",
#         "กรุณาเปลี่ยนอีเมลที่ใช้ติดต่อเป็นอีเมลใหม่ให้ด้วย",
#         "กรุณาเปลี่ยนอีเมลในระบบตามข้อมูลใหม่ด้วยครับ/ค่ะ"
#     ],
#     "response": "คุณครูสามารถแก้ไขอีเมลได้ด้วยตนเองค่ะ ทำตามขั้นตอนดังนี้\n1. ล็อกอินเข้าระบบ แล้วมาที่เมนู บัญชี ดังรูป จากนั้นระบบจะแสดงหน้าข้อมูลส่วนตัวค่ะ\n2. ทำการแก้ไขข้อมูลอีเมลให้ตรงกับระบบ ENDB จากนั้นกดบันทึก ปุ่มด้านล่างค่ะ และกดปิดหน้าข้อมูลส่วนตัว\n3. เมื่อแก้ไขอีเมลเรียบร้อยแล้ว คุณครูสามารถเข้าระบบ ENDB ด้วยอีเมลเดิมได้เลยค่ะ\nสอบถามเพิ่มเติมได้ที่ teacherpd@ipst.ac.th พร้อมแจ้งหมายเลขอ้างอิง 52006 เพื่อใช้อ้างอิงและติดตามงานค่ะ"
# }
# ]

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
#         # print(embedding_data['embeddings'][0])
#         cur.execute("INSERT INTO documents (content, embedding) VALUES (%s, %s)", (content, embedding_data['embeddings'][0]))
#         conn.commit()


content = "รีเซ็ตรหัสผ่าน"
payload = {
        "model": "mxbai-embed-large",
        "input": content
        }
        # print(payload)
response = requests.post(url, json=payload)
embedding_data = response.json()
# print(embedding_data)
# print(embedding_data['embeddings'][0])

# limit=1
# cur.execute("""
# SELECT content, embedding <-> %s::vector AS distance
# FROM documents
# ORDER BY distance
# LIMIT %s
#     """, (embedding_data['embeddings'][0], limit))

# dynamic_limit = 1 # Or whatever value you want
# cur.execute(
#     """SELECT content, 1 - (embedding <=> %s::vector) AS cosine_similarity
#         FROM documents
#         ORDER BY cosine_similarity DESC LIMIT %s""", # Added second %s
#     (embedding_data['embeddings'][0], dynamic_limit) # Now two arguments for two placeholders
# )

# import math


# num_lists_in_index = 100 # Replace with the actual 'lists' value from your index

# # Calculate a reasonable probes_value
# probes_value = int(math.sqrt(num_lists_in_index))
# dynamic_limit = 1 # Or whatever value you want

# cur.execute("SET LOCAL ivfflat.probes = %s", (probes_value,))
# cur.execute(
#     """SELECT content, 1 - (embedding <=> %s::vector) AS cosine_similarity
#         FROM documents
#         ORDER BY cosine_similarity DESC LIMIT %s""",
#     (embedding_data['embeddings'][0], dynamic_limit)
# )

# result = cur.fetchall()

# if result:
#     # เนื่องจาก limit เป็น 1 เราสามารถเข้าถึง result[0] ได้โดยตรง
#     closest_content, closest_distance = result[0]
#     print(f"\nผลลัพธ์ที่ใกล้เคียงที่สุดสำหรับ '{content}':")
#     print(f"เนื้อหา: {closest_content}")
#     print(f"ระยะทางความเหมือน (ยิ่งน้อยยิ่งเหมือน): {closest_distance:.4f}")
# else:
#     print(f"\nไม่พบผลลัพธ์ใดๆ ที่ใกล้เคียงสำหรับ '{content}'")


# cur.close()
# conn.close()



# print(f"Search results for: '{result}'")
# for i, (content, distance) in enumerate(result, 1):
#     print(f"{i}. {content} (Distance: {distance:.4f})")


    # print(payload)


#     record = KeywordEmbedding(
#         keywords=item['keywords'],
#         response=item['response'],
#         embedding=embedding
#     )
#     session.add(record)

# session.commit()
# session.close()

# print("✅ Data stored with local embedding via Ollama.")


embedding_model = OllamaEmbeddings(model="mxbai-embed-large", base_url="http://localhost:11434")

docs = [
    Document(page_content="Python is a programming language.", metadata={"source": "file1"}),
    Document(page_content="LangChain enables LLM-powered apps.", metadata={"source": "file2"}),
    Document(page_content="PGVector stores embeddings in PostgreSQL.", metadata={"source": "file3"}),
]

# # Store all documents in PGVector
vector_store = PGVector.from_documents(
    documents=docs,
    embedding=embedding_model,
    collection_name="my_documents",
    connection=DATABASE_URL,
)


# new_docs = []
# for item in data:
#     keywords_list = item["keywords"]
#     response_text = item["response"]
#     for keyword in keywords_list:
#         new_docs.append(Document(page_content=keyword, metadata={response_text}))

# new_docs = [
#     Document(page_content="Machine learning is a subset of AI.", metadata={"source": "wiki"}),
#     Document(page_content="PostgreSQL supports vector indexing.", metadata={"source": "docs"}),
# ]
results = vector_store.similarity_search("What is LangChain?", k=3)
vector_store.add_documents(new_docs)

# vectorstore = PGVector(
#     # documents=docs,
#     embeddings=embeddings,
#     # collection_name=COLLECTION_NAME,
#     connection=DATABASE_URL,
#     pre_delete_collection=True # ตั้งค่าเป็น True ถ้าต้องการลบข้อมูลเก่าใน collection ก่อนเพิ่มใหม่
# )
# # print(f"Documents added to PostgreSQL in collection '{COLLECTION_NAME}'.")

# # --- 5. ใช้ Vector Store เป็น Retriever และค้นหา ---
# # คุณสามารถปรับ k เพื่อดึงจำนวนเอกสารที่ต้องการมาตรวจสอบได้
# # retriever = vectorstore.as_retriever(search_kwargs={"k": 1}) 

# query = "ขอเปลี่ยนรหัสผ่าน"
# results = vectorstore.similarity_search(query)

# print("Retrieved documents:")
# for doc in results:
#     print(f"Content: {doc.page_content[:100]}...")
#     print(f"Metadata: {doc.metadata}")
#     print("-" * 30)



# from langchain_community.vectorstores.pgvector import PGVector
# from langchain_community.vectorstores import Lantern

# vector_store = PGVector(
#     collection_name="documents",
#     embeddings=embeddings,
#     connection=DATABASE_URL,
#     embedding_column_name="embedding",
#     content_column_name="content",
# )

# retriever = vector_store.as_retriever(search_kwargs={"k": 1}) 

# # ทำการค้นหาข้อความที่คล้ายคลึงที่สุด
# query_text = "ขอเปลี่ยนรหัสผ่าน" # คำถามที่คุณต้องการใช้ค้นหา
# retrieved_documents = retriever.invoke(query_text)

# print(f"\n--- Retrieved Documents for query: '{query_text}' ---")
# if retrieved_documents:
#     # แสดงเนื้อหาของเอกสารที่ถูกดึงมา (ซึ่งตอนนี้คือ 'ประโยคขอแก้ไขข้อมูลอีเมล')
#     print(f"Content (จากคอลัมน์ 'คำถาม'): {retrieved_documents[0].page_content}")
    
#     # แสดง metadata ซึ่งจะรวมถึงคอลัมน์ 'คำตอบ' ที่เราต้องการดู
#     print(f"Metadata (รวมถึง 'คำตอบ'): {retrieved_documents[0].metadata}")
    
#     # แสดง 'คำตอบ' ที่ตรงกันจาก metadata โดยตรง
#     if 'คำตอบ' in retrieved_documents[0].metadata:
#         print(f"**คำตอบที่เกี่ยวข้อง:** {retrieved_documents[0].metadata['คำตอบ']}")
#     else:
#         print("ไม่พบคอลัมน์ 'คำตอบ' ใน metadata ของเอกสารที่ดึงมา")
# else:
#     print("ไม่พบเอกสารสำหรับคำถามนี้")

# print("\nProcess completed.")



