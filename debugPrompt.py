import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Assuming these are defined elsewhere in your code
# from langchain.llms import OpenAI as ChatOpenAI # Example model
# from langchain.embeddings import OpenAIEmbeddings # Example embeddings
# from langchain.vectorstores import FAISS # Example vector store
# from langchain.retrievers import ArxivRetriever # Example retriever for demonstration

# --- Mocking components for demonstration if not fully defined ---
# Replace with your actual retriever and model
class MockRetriever:
    def invoke(self, query):
        if "what is AI" in query.lower():
            return [
                "Artificial intelligence (AI) is intelligence—perceiving, synthesizing, and inferring information—demonstrated by machines, as opposed to intelligence displayed by animals or humans.",
                "AI applications include advanced web search engines, recommendation systems, understanding human speech, self-driving cars, and competing at the highest level in strategic game systems (e.g., chess and Go).",
            ]
        return ["No relevant documents found."]

class MockModel:
    def invoke(self, prompt_text):
        if "Artificial intelligence" in prompt_text:
            return "AI is a field of computer science that develops intelligent machines capable of human-like thought and action."
        return "I don't know."

retriever = MockRetriever()
model = MockModel()
# --- End Mocking ---

# Set debug mode
os.environ["LANGCHAIN_DEBUG"] = "true"

template = """
Answer the question based on the context below. If you can't
answer the question, reply "I don't know".

Context: {context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

rag_chain = (
    {"context": (lambda x: x["question"]) | retriever,
     "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

print("--- Running rag_chain with debug mode ---")
question_to_ask = "What is AI?"
result = rag_chain.invoke(question_to_ask)
print(f"\nFinal Result: {result}")

# Optionally, unset debug mode after you're done
# del os.environ["LANGCHAIN_DEBUG"]