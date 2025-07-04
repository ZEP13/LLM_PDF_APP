document.addEventListener("DOMContentLoaded", () => {
  showTab("review");
});

function showTab(tabName) {
  const tabs = document.querySelectorAll(".tab-content");
  const buttons = document.querySelectorAll(".tab-menu button");

  tabs.forEach((tab) => tab.classList.remove("active"));
  buttons.forEach((btn) => btn.classList.remove("active-tab"));

  const activeTab = document.querySelector(`.${tabName}`);
  if (activeTab) activeTab.classList.add("active");

  // Trouve le bouton en fonction du nom
  buttons.forEach((btn) => {
    if (btn.textContent.toLowerCase() === tabName.toLowerCase()) {
      btn.classList.add("active-tab");
    }
  });
}

document
  .querySelectorAll(".eval_type button, .level button")
  .forEach((button) => {
    button.addEventListener("click", () => {
      const group = button.closest("ul");
      group
        .querySelectorAll("button")
        .forEach((btn) => btn.classList.remove("selected"));
      button.classList.add("selected");
    });
  });

const pdfInput = document.getElementById("pdfInput");
const pdfViewer = document.getElementById("pdfViewer");
const iaInfo3 = document.getElementById("iaInfo3");
const iaInfo = document.getElementById("iaInfo");
const prevent = document.getElementById("preventp");
const pdfTitle = document.getElementById("pdfTitle");
const pdfInstruction = document.getElementById("pdfInstruction");
const radiodiv = document.getElementById("resumeLevel");

pdfInput.addEventListener("change", () => {
  const file = pdfInput.files[0];
  if (file && file.type === "application/pdf") {
    const fileURL = URL.createObjectURL(file);
    pdfViewer.src = fileURL;
    if (pdfTitle) pdfTitle.style.display = "none";
    if (pdfInstruction) pdfInstruction.style.display = "none";
    iaInfo3.style.display = "none";
    iaInfo.style.display = "none";
    prevent.style.display = "none";
    radiodiv.style.display = "flex";
    //Active les boutons pour quizz et chat
    document.getElementById("askButton").disabled = false;
    document.getElementById("generateBtn").disabled = false;
    document.getElementById("resumeBtn").disabled = false;
  } else {
    if (pdfTitle) pdfTitle.style.display = "flex";
    if (pdfInstruction) pdfInstruction.style.display = "flex";
    pdfViewer.src = "";
    document.getElementById("askButton").disabled = true;
    document.getElementById("generateBtn").disabled = true;
    document.getElementById("resumeBtn").disabled = true;
    iaInfo3.style.display = "block";
    iaInfo.style.display = "block";
    radiodiv.style.display = "none";
    prevent.style.display = "block";
  }
});

document.getElementById("askButton").addEventListener("click", async () => {
  const input = document.getElementById("questionInput");
  const question = input.value.trim();
  const chatBox = document.getElementById("chatBox");

  if (!question) return;

  // ➤ Masquer le message d’intro IA (une seule fois)
  const iaInfo = document.getElementById("iaInfo");
  if (iaInfo) iaInfo.style.display = "none";

  // Ajouter le message utilisateur
  const userMsg = document.createElement("div");
  userMsg.className = "chat-message user";
  userMsg.textContent = question;
  chatBox.appendChild(userMsg);
  input.value = "";

  chatBox.scrollTop = chatBox.scrollHeight;

  chatBox.scrollTop = chatBox.scrollHeight;
});
