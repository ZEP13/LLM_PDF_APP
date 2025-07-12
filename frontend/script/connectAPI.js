//send the pdf to back-end when upload for optimization through other actions.
let uploadedFilename = null;

document
  .getElementById("pdfInput")
  .addEventListener("change", async function () {
    const file = this.files[0];
    if (!file) return;
    // Réinitialise le résumé, le chat et réaffiche le choix de résumé
    document.getElementById("resumeBox").innerHTML = "";
    document.getElementById("chatBox").innerHTML = "";
    document.getElementById("resumeLevel").style.display = "flex";
    document.getElementById("resumeBtnBox").style.display = "flex";
    document.getElementById("eval_type").style.display = "block";
    document.getElementById("level").style.display = "block";
    document.getElementById("generateBtn").style.display = "block";
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
  document.getElementById("resumeBtnBox").style.display = "none";
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
  const resumeText = data.resume || "";
  document.getElementById("resumeBox").innerHTML = resumeText;
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
  aiMsg.innerHTML =
    reponseAI.AI_answer || reponseAI.error || JSON.stringify(reponseAI);
  chatBox.appendChild(aiMsg);
}

// Générer le QCM
async function generateQCM() {
  if (!uploadedFilename) {
    alert("Aucun fichier PDF n'a été uploadé.");
    return;
  }

  const level = document.querySelector('input[name="levelqcm"]:checked')?.value;
  const type = document.querySelector('input[name="typeqcm"]:checked')?.value;

  document.getElementById("eval_type").style.display = "none";
  document.getElementById("level").style.display = "none";
  document.getElementById("generateBtn").style.display = "none";

  if (!level || !type) {
    alert("Veuillez sélectionner un niveau et un type de QCM.");
    return;
  }

  const url = `http://localhost:8000/qcm?filename=${encodeURIComponent(
    uploadedFilename
  )}&levelqcm=${encodeURIComponent(level)}&typeqcm=${encodeURIComponent(type)}`;

  try {
    const response = await fetch(url);
    const data = await response.json();

    // if (data.error) {
    //   alert("Erreur : " + data.error);
    //   return;
    // }

    console.log("QCM généré :", data.QCM);
    displayQCM(data.QCM);
  } catch (err) {
    console.error("Erreur lors de l'appel à l'API QCM :", err);
  }
}
function displayQCM(qcmData) {
  const container = document.getElementById("testBox");
  container.style.display = "flex";
  container.style.flexDirection = "column";
  container.innerHTML = ""; // Reset au cas où on regénère

  qcmData.forEach((item, index) => {
    const questionBlock = document.createElement("div");
    questionBlock.className = "question-block";
    questionBlock.innerHTML = `<p><strong>Q${index + 1}:</strong> ${
      item.question
    }</p> <br/>`;

    item.propositions.forEach((choice, i) => {
      const letter = ["A", "B", "C"][i];
      const id = `q${index}_opt${i}`;
      questionBlock.innerHTML += `
        <label>
          <input type="radio" name="q${index}" value="${choice}" id="${id}" />
          ${letter}. ${choice}
        </label><br>`;
    });

    // Champ caché pour stocker la bonne réponse
    const correctAnswer = document.createElement("input");
    correctAnswer.type = "hidden";
    correctAnswer.value = item.réponse;
    correctAnswer.classList.add("correct-answer");
    questionBlock.appendChild(correctAnswer);

    container.appendChild(questionBlock);
  });

  // Bouton Corriger
  const corrigerBtn = document.createElement("button");
  corrigerBtn.innerText = "Corriger";
  corrigerBtn.id = "corrigerBtn";
  corrigerBtn.onclick = () => corrigerQCM(qcmData.length);
  container.appendChild(corrigerBtn);
}

function corrigerQCM(totalQuestions) {
  let score = 0;

  for (let i = 0; i < totalQuestions; i++) {
    const selected = document.querySelector(`input[name="q${i}"]:checked`);
    const correct = document
      .querySelectorAll(".question-block")
      [i].querySelector(".correct-answer").value;

    const questionBlock = document.querySelectorAll(".question-block")[i];

    const result = document.createElement("div");
    result.className = "correction";

    if (selected) {
      if (selected.value === correct) {
        result.innerHTML = `<span style="color: green;">✔ Bonne réponse</span>`;
        score++;
      } else {
        result.innerHTML = `<span style="color: red;">✘ Mauvaise réponse. Réponse correcte : ${correct}</span>`;
      }
    } else {
      result.innerHTML = `<span style="color: red;">✘ Non répondu. Réponse correcte : ${correct}</span>`;
    }

    // Supprimer ancienne correction s'il y en a une
    const oldResult = questionBlock.querySelector(".correction");
    if (oldResult) oldResult.remove();

    questionBlock.appendChild(result);
  }

  // Score final
  const scoreBlock = document.createElement("div");
  scoreBlock.innerHTML = `<h3>Score : ${score} / ${totalQuestions}</h3>`;
  document.getElementById("testBox").appendChild(scoreBlock);
}
