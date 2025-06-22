from googletrans import Translator
# import ollama
# from langchain_ollama import OllamaLLM, OllamaEmbeddings
# from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document
import pandas as pd
import asyncio
# import google.genai as genai
# import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_postgres import PGVector

from langchain_core.prompts import ChatPromptTemplate # เพิ่ม
from langchain_core.output_parsers import StrOutputParser # เพิ่ม
from langchain_core.runnables import RunnablePassthrough # เพิ่ม
from langchain_ollama import OllamaLLM, OllamaEmbeddings, ChatOllama # เพิ่ม ChatOllama
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    filter_messages,
)
from sqlalchemy import create_engine
from operator import itemgetter

# vector_store.add_documents(docs)

from langchain_core.prompts import ChatPromptTemplate # เพิ่ม
from translate import  translate_text_googletrans,main

# text_to_translate_thai = "สวัสดีครับ คุณสบายดีไหม" # Hello, how are you? (Thai)
# text_to_translate_french = "Bonjour, comment ça va ?" # Hello, how are you? (French)

model = OllamaLLM(model="llama3", temperature=0.0, base_url="http://192.168.1.53:11434")
embeddings = OllamaEmbeddings(model="mxbai-embed-large", base_url="http://192.168.1.53:11434")


engine = create_engine("postgresql+psycopg2://myuser:mypassword@localhost:5433/mydatabase")

async def run_translation_example(text_to_translate_thai):
    # text_to_translate_thai = "ขอเปลี่ยนรหัสผ่าน"
    print(f"Original Thai text: {text_to_translate_thai}")

    # Await the imported async function
    translated_thai_to_english = await translate_text_googletrans(text_to_translate_thai, dest_language='en')

    if translated_thai_to_english:
        return translated_thai_to_english
    else:
        print("Translation failed.")

async def gen_answer(text_input):

    # --- 2. กำหนดค่าการเชื่อมต่อ PostgreSQL ---
    DB_USER = "myuser"
    DB_PASSWORD = "mypassword"
    DB_HOST = "localhost"
    DB_PORT = "5433"
    DB_NAME = "mydatabase"
    CONNECTION_STRING = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # Translate Thai to English (auto-detect source)
    vectorstore = PGVector(
    connection=engine,
    embeddings=embeddings,
    collection_name='my_docs',
    # pre_delete_collection=True # ตั้งค่าเป็น True ถ้าต้องการลบข้อมูลเก่าใน collection ก่อนเพิ่มใหม่
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1}) 

    template = """
    Answer the question based on the context below. If you can't 
    answer the question, reply "I don't know".

    Context: {context}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
    {"context":  retriever , # Retrieve documents and format them as context
    "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
    )

    translation_prompt = ChatPromptTemplate.from_template(
    "Translate {answer} to Thai"
    )

    translation_chain = (
    {"answer": rag_chain } | translation_prompt | model | StrOutputParser()
    )

    test_queries = [
        "ต้องการรีเซ็ตรหัสผ่าน",
        "How do I change my password for the first time?",
        "I want to change the contact email to this new one",
        "เปลี่ยนอีเมล์",
        # Add more specific queries based on your CSV content
    ]

    translated_thai_to_english = await run_translation_example(text_input)
    input_data = {"language": "Thai", "question": translated_thai_to_english}
    print(f"\n--- Generating Answer with RAG for query: '{input_data['question']}' ---")
    translated_answer = translation_chain.invoke(translated_thai_to_english)
    print(translated_answer)
    return translated_answer


# if __name__ == "__main__":
#     for query_text in test_queries:
#         translated_thai_to_english = asyncio.run(run_translation_example(query_text))
#         input_data = {"language": "Thai", "question": translated_thai_to_english}
#         print(f"\n--- Generating Answer with RAG for query: '{input_data['question']}' ---")
#         translated_answer = translation_chain.invoke(input_data)
#         print(translated_answer)
