import os
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaLLM


def summarize_pdf(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load_and_split()
    model = OllamaLLM(model='llama3.1')

    chain = load_summarize_chain(model, chain_type='map_reduce')
    summary = chain.invoke(docs)

    return summary

if __name__ == "__main__":
    print(summarize_pdf('backend/CV_2024_2.pdf'))

    print('\n')
    summarize = summarize_pdf('backend/CV_2024_2.pdf')
    print('resume: ',summarize['output_text'])
