from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaLLM


class QCM:
    def __init__(self,model_name="llama3.1"):
        self.model = OllamaLLM(model=model_name)


    def qcm(self, filename:str, levelqcm: int, typeqcm: int):
        loader = PyPDFLoader(filename)
        documents = loader.load()
        content = "\n".join([doc.page_content for doc in documents])

        level = ["collégien", "universitaire"]
        type = ["connaissance", "compréhension, application"]
        prompt = f"""
            Tu es un générateur de QCM à partir de documents.

            Tu dois générer exactement 5 questions à choix multiples avec 3 propositions chacune (A, B, C), et indiquer clairement la bonne réponse.

            ⚠️ Ta réponse doit être au format JSON strict uniquement.
            Retourne uniquement un tableau JSON, sans clé, sans texte avant/après, sans commentaires.

            Voici un exemple de format :

            [
            {{
                "question": "Quel est le format requis pour imprimer un billet de train?",
                "propositions": [
                "Format A3, noir et blanc",
                "Format A4, couleur ou noir et blanc",
                "Format lettre, écran"
                ],
                "réponse": "Format A4, couleur ou noir et blanc"
            }},
            ...
            ]

            Niveau de difficulté : {level[levelqcm - 1]}
            Type : {type[typeqcm - 1]}

            Voici le contenu extrait du PDF (tronqué) :
            \"\"\"
            {content[:3000]}
            \"\"\"
            """



        response = self.model.invoke(prompt)
        return response