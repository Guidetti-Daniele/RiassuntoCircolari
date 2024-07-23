const documents = document.querySelectorAll(".document-row");
const submitBtn = document.querySelector(".submit-btn");

function selectDocument(event) {
  const selected = event.target.closest(".document-row");

  documents.forEach((document) => {
    if (document.classList.contains("document-selected")) {
      document.classList.remove("document-selected");
      return;
    }
  });

  selected.classList.add("document-selected");
  submitBtn.removeAttribute("disabled");
}

documents.forEach((document) => {
  document.addEventListener("click", (event) => selectDocument(event));
});
