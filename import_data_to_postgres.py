
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


# csv_file_path = "faq_100_questions.csv" # ตรวจสอบพาธของไฟล์ CSV ของคุณ

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


data = [
    {
        "keywords": [
            "Please update the email in my profile.",
            "Kindly help correct my email address.",
            "Please update the email address in my profile to the current one.",
            "Please correct the registered email address in the system.",
            "Please update the registered email address to be current.",
            "Please correct my email information.",
            "Please update my email information to the latest one.",
            "Please change the email address to the correct one.",
            "I want to update the email linked to this account.",
            "I want to correct the email used in the system. Please assist.",
            "I want to change the contact email to this one.",
            "I want to change the contact email to this new one.",
            "I want to change the email in the system to [new email].",
            "I want to change the email used in the account.",
            "Please update my email to the new one.",
            "Please update the new email in the system.",
            "Please update the email in my account.",
            "Please update the email address in the system to match the new one.",
            "Please correct the email in the system to match the latest information.",
            "Please change the email in the system to this new one.",
            "Please update my email to the new one as informed.",
            "Please replace the email in the system with this new one.",
            "Please replace the email in the system with this one.",
            "I found that my email information is incorrect. Please fix it.",
            "I would like to change the email in my user account.",
            "I request to update my email in the system to replace the old one.",
            "I kindly request correction of the incorrect email in the system.",
            "I would appreciate your cooperation in correcting the email in the user account.",
            "Kindly update the email in my profile to the correct one.",
            "Kindly correct the email in the system.",
            "Please update the old email to the following new one.",
            "Sorry to bother you, but please help update my email.",
            "I would like to update the registered email to a new one.",
            "Please change the contact email to the new one.",
            "Please replace the email in the system with this one.",
            "Please verify and correct the email address.",
            "Please help correct the email address with the new information.",
            "Please change the email in the system to the new one.",
            "Please change the contact email to the new one.",
            "Please change the system email to the new information."
        ],
        "response": "You can update your email by yourself. Please follow these steps:\n1. Log into the system, then go to the 'Account' menu as shown. The system will display your profile page.\n2. Update your email address to match the one used in the ENDB system, then click the 'Save' button at the bottom. After saving, close the profile page.\n3. Once the email is updated, you can continue to access the ENDB system using your existing login.\nIf you need further assistance, please contact teacherpd@ipst.ac.th and mention reference number 52006 for tracking and support."
    }
]

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
docs = []
for item in data:
    keywords_list = item["keywords"]
    response_text = item["response"]
    for keyword in keywords_list:
        content = "Question: " + keyword + "Answer: " + response_text
        docs.append(Document(page_content=content))



vector_store = PGVector(
    # documents=docs,
    embeddings=embeddings,
    collection_name="my_docs",
    connection=CONNECTION_STRING,
)

vector_store.add_documents(docs)
