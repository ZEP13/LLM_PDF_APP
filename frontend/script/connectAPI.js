//send the pdf to back-end when upload for optimization through other actions.
let uploadedFilename = null;

document
  .getElementById("pdfInput")
  .addEventListener("change", async function () {
    const file = this.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload-pdf/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errText = await response.text();
        console.error("Échec de l'upload :", errText);
        return;
      }

      const data = await response.json();
      uploadedFilename = data.filename;
      console.log("PDF upload: ", data);

      // const fileURL = URL.createObjectURL(file);
      // document.getElementById("pdfViewer").src = fileURL;
    } catch (err) {
      console.error("Upload error:", err);
    }
  });

//call pdf resume function from resumePDF onclick
async function resumePDF() {
  if (!uploadedFilename) {
    alert("Aucun fichier uploadé");
    return;
  }

  document.getElementById("resumeLevel").style.display = "none";

  // Obtenir la valeur sélectionnée
  const level_prompt = document.querySelector(
    'input[name="resumeNiveau"]:checked'
  )?.value;

  if (!level_prompt) {
    alert("Veuillez sélectionner un niveau de résumé.");
    return;
  }

  const response = await fetch(
    `http://localhost:8000/resume?level=${encodeURIComponent(
      level_prompt
    )}&filename=${encodeURIComponent(uploadedFilename)}`
  );

  if (!response.ok) {
    console.log("Erreur lors de la génération du résumé PDF");
    return;
  }

  const data = await response.json();
  console.log("Résumé :", data);
}

//ask ia about pdf details
async function chat() {
  message = document.getElementById("questionInput").value;

  console.log(message);

  const reponse = await fetch(`http://localhost:8000/chat/`, {
    method: "POST",
    body: message,
  });

  if (!reponse.ok) {
    console.log("erreur evoi message");
  }

  const reponseAI = await reponse.json();

  console.log("IA say: ", reponseAI);

  const aiMsg = document.createElement("div");
  aiMsg.className = "chat-message ai";
  aiMsg.textContent = reponseAI;
  chatBox.appendChild(aiMsg);
}
