import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()


class Chat():
    def __init__(self,model_name="llama3.1"):

        self.model = OllamaLLM(model=model_name)

    def setup_qa_systeme(self, file_path, message_user):
        loader = PyPDFLoader(file_path)
        docs = loader.load_and_split()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs)

        embeddings = OllamaEmbeddings(self.model)
        vector_store = FAISS.from_documents(chunks, embeddings)

        retriever = vector_store.as_retriever()

        qa_chain = RetrievalQA.from_chain_type(self.model, retriever=retriever)

        return qa_chain



# if __name__ == "__main__":

#     qa_chain = setup_qa_systeme('CV_2024_2.pdf')

#     while True:
#         question = input("\n Ask question: ")
#         if question.lower() == "exit":
#              break
#         answer= qa_chain.invoke(question)

#         print('reponse:')
#         print(answer['result'])








# template= """
# Answer the question bellow.

# here is the conversation hystory: {context}

# question: {question}

# """

# model = OllamaLLM(model="llama3.1")
# prompt = ChatPromptTemplate.from_template(template)

# chain = prompt | model

# def handle_conv():
#     context =""
#     print("exit by typing 'exit'")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == "exit":
#             break

#         response = chain.invoke({"context": context, "question": user_input})

#         print("Bot: ", response)

#         context += f"\nUser: {user_input}\nAi: {response}"


# if __name__ == "__main__":
#     handle_conv()
