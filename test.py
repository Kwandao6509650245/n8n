import ollama
from langchain_ollama import OllamaLLM, OllamaEmbeddings
# from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document
import pandas as pd

from langchain_core.prompts import ChatPromptTemplate # เพิ่ม
from langchain_core.output_parsers import StrOutputParser # เพิ่ม
from langchain_core.runnables import RunnablePassthrough # เพิ่ม
from langchain_ollama import OllamaLLM, OllamaEmbeddings, ChatOllama # เพิ่ม ChatOllama


# --- 1. กำหนดค่า Ollama ---
# ใช้ OllamaLLM เมื่อคุณต้องการแค่ดึงข้อความ ไม่ได้ใช้คุณสมบัติ Chat Model เต็มรูปแบบ
model = OllamaLLM(model="llama3", temperature=0.0, base_url="http://localhost:11434")
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

engine = create_engine("postgresql+psycopg2://myuser:mypassword@localhost:5432/mydatabase")


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

print("\n Normal Process completed.")
print("------------------------------------------------")

template = """
คุณเป็น AI Assistant ที่ตอบคำถามจาก context ที่ให้มา

กฎสำคัญ:
1. ตอบเป็นภาษาเดียวกับคำถาม (ไทย→ไทย, อังกฤษ→อังกฤษ)
2. ใช้ข้อมูลจาก context เท่านั้น หากไม่มีข้อมูลให้แจ้ง
3. คำถามเดียวกันในภาษาต่างกัน = คำตอบเดียวกัน
4. ดู keyword ว่าคำถามถามเรื่องอะไร ตอบให้ตรง keyword

รูปแบบการตอบ:
- คำถามขั้นตอน: แสดงเป็น 1, 2, 3...

Context (Relevant information from the knowledge base):
{context}

Question (User's question):
{question}

Answer (Your response):
"""
prompt = ChatPromptTemplate.from_template(template)

# 3. Define how to format the retrieved documents for the context
def format_docs_for_context(docs):
    formatted_string = ""
    for doc in docs:
        # Extract 'answer' from metadata (assuming 'คำตอบ' is now 'answer' in English metadata)
        answer_content = doc.metadata.get('คำตอบ', 'No answer information found') 
        # page_content is the 'question' we use for embedding
        question_content = doc.page_content 
        
        formatted_string += f"Question: {question_content}\n"
        formatted_string += f"Answer: {answer_content}\n\n"
    return formatted_string.strip() # Remove trailing whitespace

# 4. Construct the RAG Chain
rag_chain = (
    {"context": retriever | format_docs_for_context, # Retrieve documents and format them as context
    "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# # --- 5. Use RAG Chain to Get Answer from AI ---
# query_text_rag = "I would like to update the registered email to a new one." # The question for RAG
# print(f"\n--- Generating Answer with RAG for query: '{query_text_rag}' ---")
# final_answer = rag_chain.invoke(query_text_rag)

# print(final_answer)

# print("\nProcess completed.")

# --- 6. Use RAG Chain to Get Answer from AI ---

test_queries = [
    "ต้องการรีเซ็ตรหัสผ่าน",
    "How do I change my password for the first time?",
    "I want to change the contact email to this new one",
    "เปลี่ยนอีเมล์",
    # Add more specific queries based on your CSV content
]

for query_text in test_queries:
    print(f"\n--- Generating Answer with RAG for query: '{query_text}' ---")
    final_answer = rag_chain.invoke(query_text)
    print(final_answer)
    print("-" * 50) # Separator for readability

print("\nProcess completed.")