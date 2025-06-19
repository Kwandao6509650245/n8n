
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
DB_PORT = "5432"
DB_NAME = "mydatabase"
CONNECTION_STRING = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# COLLECTION_NAME = "my_ollama_documents_collection"

from langchain_postgres import PGVector

# model = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
embeddings = OllamaEmbeddings(model="mxbai-embed-large", base_url="http://localhost:11434")


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

vector_store = PGVector(
    # documents=docs,
    embeddings=embeddings,
    collection_name="my_docs",
    connection=CONNECTION_STRING,
)



vector_store.add_documents(docs)
