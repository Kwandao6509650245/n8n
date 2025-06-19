import ollama
from langchain_ollama import OllamaLLM, OllamaEmbeddings
# from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document
import pandas as pd

# --- 1. กำหนดค่า Ollama ---
# ใช้ OllamaLLM เมื่อคุณต้องการแค่ดึงข้อความ ไม่ได้ใช้คุณสมบัติ Chat Model เต็มรูปแบบ
model = OllamaLLM(model="llama3.2", base_url="http://localhost:11434")
embeddings = OllamaEmbeddings(model="mxbai-embed-large", base_url="http://localhost:11434")

# --- 2. กำหนดค่าการเชื่อมต่อ PostgreSQL ---
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "mydatabase"
CONNECTION_STRING = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# COLLECTION_NAME = "my_ollama_documents_collection"

from langchain_postgres import PGVector

# model = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
embeddings = OllamaEmbeddings(model="mxbai-embed-large", base_url="http://localhost:11434")


print(f"Connecting to: {CONNECTION_STRING}")

# docs = [
#     Document(page_content="LangChain is an open-source framework for LLMs."),
#     Document(page_content="PGVector is a PostgreSQL extension for vector search."),
# ]

# vector_store = PGVector(
#     # documents=docs,
#     embeddings=embeddings,
#     collection_name="test",
#     connection=CONNECTION_STRING,
# )



# vector_store.add_documents(docs)

# --- 3. ดึงข้อมูลจากไฟล์ CSV และเตรียม LangChain Documents ---
# csv_file_path = "my_doc.csv" # ตรวจสอบพาธของไฟล์ CSV ของคุณ

# try:
#     df = pd.read_csv(csv_file_path, encoding='utf-8')
# except FileNotFoundError:
#     print(f"Error: File not found at {csv_file_path}")
#     exit()

# docs = []
# # กำหนดชื่อคอลัมน์ที่เป็นเนื้อหาหลักที่คุณต้องการให้ AI ใช้ค้นหา
# # *** ต้องตรงกับชื่อคอลัมน์ในไฟล์ CSV ของคุณเป๊ะๆ ***
# content_column = 'คำถาม' 

# for index, row in df.iterrows():
#     # ตรวจสอบว่าคอลัมน์เนื้อหาหลักไม่ว่าง
#     if pd.isna(row[content_column]):
#         continue # ข้ามแถวที่ไม่มีเนื้อหาหลัก

#     page_content = str(row[content_column])
    
#     # สร้าง metadata จากคอลัมน์อื่นๆ ทั้งหมด ยกเว้นคอลัมน์เนื้อหาหลัก
#     # ในกรณีนี้ 'คำตอบ' จะถูกเก็บใน metadata ของเอกสาร
#     metadata = row.drop(content_column).to_dict() 

#     docs.append(Document(page_content=page_content, metadata=metadata))

# print(f"Loaded {len(docs)} documents from CSV.")

# # --- 4. สร้าง Vector Store และบันทึกข้อมูลลง PostgreSQL ---
# print("Connecting to PGVector store and adding documents...")
# # 'pre_delete_collection=True' จะลบ collection เก่าก่อนเพิ่มใหม่เสมอ
# vector_store = PGVector.from_documents(
#     documents=docs,
#     embedding=embeddings,
#     collection_name="state_of_union_vectors",
#     connection=CONNECTION_STRING,
# )

# vector_store.create_tables_if_not_exists()

from sqlalchemy import create_engine

# vector_store.add_documents(docs)

from langchain_core.prompts import ChatPromptTemplate # เพิ่ม

engine = create_engine("postgresql+psycopg2://myuser:mypassword@localhost:5433/mydatabase")


vectorstore = PGVector(
    connection=engine,
    embeddings=embeddings,
    collection_name='my_docs',
    # pre_delete_collection=True # ตั้งค่าเป็น True ถ้าต้องการลบข้อมูลเก่าใน collection ก่อนเพิ่มใหม่
)

csv_file_path = "my_doc.csv" # ตรวจสอบพาธของไฟล์ CSV ของคุณ

try:
    df = pd.read_csv(csv_file_path, encoding='utf-8')
except FileNotFoundError:
    print(f"Error: File not found at {csv_file_path}")
    exit()

docs = []
# กำหนดชื่อคอลัมน์ที่เป็นเนื้อหาหลักที่คุณต้องการให้ AI ใช้ค้นหา
# *** ต้องตรงกับชื่อคอลัมน์ในไฟล์ CSV ของคุณเป๊ะๆ ***
content_column = 'คำถาม' 

for index, row in df.iterrows():
    # ตรวจสอบว่าคอลัมน์เนื้อหาหลักไม่ว่าง
    if pd.isna(row[content_column]):
        continue # ข้ามแถวที่ไม่มีเนื้อหาหลัก

    page_content = str(row[content_column])
    
    # สร้าง metadata จากคอลัมน์อื่นๆ ทั้งหมด ยกเว้นคอลัมน์เนื้อหาหลัก
    # ในกรณีนี้ 'คำตอบ' จะถูกเก็บใน metadata ของเอกสาร
    metadata = row.drop(content_column).to_dict() 

    docs.append(Document(page_content=page_content, metadata=metadata))

print(f"Loaded {len(docs)} documents from CSV.")

# --- 4. สร้าง Vector Store และบันทึกข้อมูลลง PostgreSQL ---
print("Connecting to PGVector store and adding documents...")
# 'pre_delete_collection=True' จะลบ collection เก่าก่อนเพิ่มใหม่เสมอ
# vectorstore = PGVector.from_documents(
#     documents=docs,
#     embedding=embeddings,
#     collection_name='test',
#     connection=engine,
#     pre_delete_collection=True # ตั้งค่าเป็น True ถ้าต้องการลบข้อมูลเก่าใน collection ก่อนเพิ่มใหม่
# )
# print(f"Documents added to PostgreSQL in collection '{test}'.")

retriever = vectorstore.as_retriever(search_kwargs={"k": 2}) 

query_text = "Do I need to use the email-provided password before setting a new one?"
retrieved_documents = retriever.invoke(query_text)

print(f"\n--- Retrieved Documents for query: '{query_text}' ---")
if retrieved_documents:
    # แสดงเนื้อหาของเอกสารที่ถูกดึงมา (ซึ่งตอนนี้คือ 'ประโยคขอแก้ไขข้อมูลอีเมล')
    print(f"Content : {retrieved_documents[0].page_content}")

else:
    print("ไม่พบเอกสารสำหรับคำถามนี้")

print("\nProcess completed.")