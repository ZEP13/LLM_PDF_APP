import os
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate



prompt = [
    """Résume ce document de façon simple et classique. Reste strictement fidèle au contenu du PDF. 
    Structure la réponse en HTML vivant : utilise des balises <ul>, <ol>, <li> pour les listes, <p> pour les paragraphes, <h2>/<h3> pour les titres, et ajoute des alinéas (text-indent) pour les paragraphes. Mets en valeur les mots importants avec <strong> ou <em>.
Ajoute des listes à puces ou numérotées pour les points clés..""",
    """Résume ce document pour un collégien. Indique à chaque fois où tu as trouvé l'information dans le PDF (ex : page ou paragraphe).
    Structure la réponse en HTML vivant : utilise des balises <ul>, <ol>, <li> pour les listes, <p> pour les paragraphes, <h2>/<h3> pour les titres, et ajoute des alinéas (text-indent) pour les paragraphes. Mets en valeur les mots importants avec <strong> ou <em>.
Ajoute des listes à puces ou numérotées pour les points clés..""",
    """Fais un résumé universitaire très complet et structuré. Sois détaillé, rigoureux et spécifie à chaque fois l’origine des propos (page/paragraphe du PDF).
    Structure la réponse en HTML vivant : utilise des balises <ul>, <ol>, <li> pour les listes, <p> pour les paragraphes, <h2>/<h3> pour les titres, et ajoute des alinéas (text-indent) pour les paragraphes. Mets en valeur les mots importants avec <strong> ou <em>.
Ajoute des listes à puces ou numérotées pour les points clés.."""
]

class PDFSummarizer:
    def __init__(self, model_name="llama3.1"):
        self.model = OllamaLLM(model=model_name)

    def summarize_pdf(self, file_path, prompt_style):

        prompt_template = PromptTemplate.from_template(prompt[prompt_style] + "\n\n{text}")

        chain = load_summarize_chain(self.model, 
                                     chain_type='stuff', prompt=prompt_template)
        
        loader = PyPDFLoader(file_path)

        docs = loader.load_and_split()
        summary = chain.invoke(docs)
        return summary
