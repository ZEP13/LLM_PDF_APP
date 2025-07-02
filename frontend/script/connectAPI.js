//send the pdf to back-end when upload for optimization through other actions.
let uploadedFilename = null;

document
  .getElementById("pdfInput")
  .addEventListener("change", async function () {
    const file = this.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const reponse = await fetch("http://localhost:8000/upload-pdf/", {
      method: "POST",
      body: formData,
    });
    const data = await reponse.json();
    uploadedFilename = data.filename;
    console.log("PDF upload: ", data);
  });

//call pdf resume function from resumePDF onclick
async function resumePDF() {
  if (!uploadedFilename) {
    alert("Aucun fichier uploadé");
    return;
  }

  const reponse = fetch(
    `http://localhost:8000/resume?filename=${encodeURIComponent(
      uploadedFilename
    )}`
  );
  if (!reponse) {
    console.log("aucun fichier selectionne pdf");
  }

  const data = await reponse.json();
  console.log("resume :", data);
}
