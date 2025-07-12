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

        self.retriever = vector_store.as_retriever(search_kwargs={"k": 5})


        self.template = """
            You are an assistant answering questions based on a PDF.

            Only if you're sure the answer is not in the PDF, then respond:
            "The PDF doesn't contain enough information to answer this question."
            Otherwise, provide the most accurate answer possible using the given context.

            Structure la réponse en HTML vivant : utilise des balises <ul>, <ol>, <li> pour les listes, <p> pour les paragraphes, <h2>/<h3> pour les titres, et ajoute des alinéas (text-indent) pour les paragraphes. Mets en valeur les mots importants avec <strong> ou <em>.
            Ajoute des listes à puces ou numérotées pour les points clés.
                        
            Conversation history:
            {history}

            Context from PDF:
            {context}

            Question:
            {question}


        """


        self.prompt = ChatPromptTemplate.from_template(self.template)

    def chat(self, question_user: str) -> str:
        
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
