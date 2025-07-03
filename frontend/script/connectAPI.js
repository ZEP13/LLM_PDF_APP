//send the pdf to back-end when upload for optimization through other actions.
let uploadedFilename = null;

document
  .getElementById("pdfInput")
  .addEventListener("change", async function (e) {
    e.preventDefault(); // prevents default behavior (if any)
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
        console.error("Upload failed");
        return;
      }

      const data = await response.json();
      uploadedFilename = data.filename;
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

  const reponse = await fetch(
    `http://localhost:8000/resume?filename=${encodeURIComponent(
      uploadedFilename
    )}`
  );
  if (!reponse.ok) {
    console.log("aucun fichier selectionne pdf");
    return;
  }

  const data = await reponse.json();
  console.log("resume :", data);
}

//ask ia about pdf details

async function chat() {
  message = document.getElementById("questionInput").value;

  console.log(message);

  const reponse = fetch(`http://localhost:8000/chat/`, {
    method: "POST",
    body: { message, uploadedFilename },
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
