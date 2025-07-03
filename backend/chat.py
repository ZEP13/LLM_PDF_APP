from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
load_dotenv()


class Chat():
    def __init__(self,model_name="llama3.1"):
        self.chain = None
        self.model = OllamaLLM(model=model_name)
        self.history  = ""
    def setup_qa_systeme(self, file_path: str):
        loader = PyPDFLoader(file_path)
        docs = loader.load_and_split()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs)

        texts = [doc.page_content for doc in chunks]  
        embeddings = OllamaEmbeddings(model='llama3.1') 
        vector_store = FAISS.from_texts(texts, embeddings)  

        self.retriever = vector_store.as_retriever()


        self.template = """
            You are an assistant answering questions based on a PDF.

            If the answer is not in the PDF, reply:
            "The PDF doesn't have the information to answer this question."

            Conversation history:
            {history}

            Context from PDF:
            {context}

            Question:
            {question}
        """


        self.prompt = ChatPromptTemplate.from_template(self.template)

        self.chain = RetrievalQA.from_chain_type(llm=self.model, retriever=self.retriever)

    def chat(self, question_user: str) -> str:
        if not self.chain:
            raise ValueError("La chaîne QA n'est pas initialisée. Appelle setup_qa_systeme d'abord.")
        
        docs = self.retriever.invoke(question_user)
        context = "\n".join([doc.page_content for doc in docs])

        # Construis input pour le prompt
        prompt_input = {
            "history": self.history,
            "context": context,
            "question": question_user,
        }
        final_prompt = self.prompt.format(**prompt_input) # remplace par les données dans template

        answerai = self.model.invoke(final_prompt)
        
        self.history  += f"\nUser: {question_user}\nAi: {answerai}"
        
        return answerai


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
