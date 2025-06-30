from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


template= """
Answer the question bellow.

here is the conversation hystory: {context}

question: {question}

"""

model = OllamaLLM(model="llama3.1")
prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

def handle_conv():
    context =""
    print("exit by typing 'exit'")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = chain.invoke({"context": context, "question": user_input})

        print("Bot: ", response)

        context += f"\nUser: {user_input}\nAi: {response}"


if __name__ == "__main__":
    handle_conv()
