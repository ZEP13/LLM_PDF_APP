//send the pdf to back-end when upload for optimization through other actions.
let uploadedFilename = null;

document
  .getElementById("pdfInput")
  .addEventListener("change", async function () {
    const file = this.files[0];
    if (!file) return;

    // Envoi du PDF au backend
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
      console.log("uploadedFilename:", uploadedFilename);
      console.log("PDF upload: ", data);
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
    `http://localhost:8000/resume?level_prompt=${encodeURIComponent(
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
  const message = document.getElementById("questionInput").value;
  const chatBox = document.getElementById("chatBox");

  if (!uploadedFilename) {
    alert("Aucun fichier PDF n'a été uploadé.");
    return;
  }
  if (!message) {
    alert("Veuillez entrer une question.");
    return;
  }

  console.log(message);

  // Envoyer la question et le nom du fichier en query string
  const url = `http://localhost:8000/chat/?question_user=${encodeURIComponent(
    message
  )}&filename=${encodeURIComponent(uploadedFilename)}`;

  const reponse = await fetch(url, {
    method: "POST",
  });

  if (!reponse.ok) {
    console.log("erreur evoi message");
  }

  const reponseAI = await reponse.json();

  console.log("IA say: ", reponseAI);

  const aiMsg = document.createElement("div");
  aiMsg.className = "chat-message ai";
  // Affiche la réponse AI proprement
  aiMsg.textContent =
    reponseAI.AI_answer || reponseAI.error || JSON.stringify(reponseAI);
  chatBox.appendChild(aiMsg);
}
