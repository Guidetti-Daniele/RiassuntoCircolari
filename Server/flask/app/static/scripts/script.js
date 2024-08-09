document.addEventListener("DOMContentLoaded", function () {
  setupFieldSelect("recipient", "/get-destin");
  setupFieldSelect("class", "/get-class");
  setupFieldSelect("type", "/get-types");
  setupDocumentSelect();
  setupSubmitButton();
});

function addOptions(select, text, value) {
  const option = new Option(text, value);
  select.appendChild(option);
}

async function setupFieldSelect(elementId, endpoint) {
  try {
    const response = await fetch(endpoint);
    const data = await response.json();

    const fieldSelect = document.getElementById(elementId);

    data
      .filter((item) => item !== "#separator#")
      .forEach((item) => addOptions(fieldSelect, item, item));
  } catch (error) {
    console.error("Error", error);
  }
}

async function fetchDocumentData(endpoint, data) {
  const queryString = Object.keys(data)
    .map((key) => encodeURIComponent(key) + "=" + encodeURIComponent(data[key]))
    .join("&");

  const resource = `${endpoint}?${queryString}`;
  const options = {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  };

  try {
    const response = await fetch(resource, options);
    const data = await response.json();

    const documentSelect = document.getElementById("document");
    const submitBtn = document.getElementById("submit-btn");

    documentSelect.innerHTML = "";

    if (data.length === 0) submitBtn.setAttribute("disabled", "");
    else data.forEach((item) => addOptions(documentSelect, item[1], item[0]));
  } catch (error) {
    console.error("Error", error);
  }
}

function setupDocumentSelect() {
  const triggers = ["type", "recipient", "class"];
  const documentSelect = document.getElementById("document");
  const submitBtn = document.getElementById("submit-btn");

  triggers.forEach((trigger) => {
    const fieldSelect = document.getElementById(trigger);

    fieldSelect.addEventListener("change", () => {
      const type = document.getElementById("type").value;
      const recipient = document.getElementById("recipient").value;
      const class_ = document.getElementById("class").value;

      if (type && recipient && class_) {
        const data = { dest: recipient, class: class_, type: type };
        fetchDocumentData("/get-circ", data);
      }
    });
  });

  documentSelect.addEventListener("change", (event) => {
    if (event.target.value) submitBtn.removeAttribute("disabled");
  });
}

function setupSubmitButton() {
  const submitBtn = document.getElementById("submit-btn");
  const markdownDisplay = document.getElementById("markdownDisplay");

  submitBtn.addEventListener("click", async () => {
    const hash = document.getElementById("document").value;
    const type = document.getElementById("type").value;

    if (hash && type) {
      try {
        const resource = `/get-text?hash=${encodeURIComponent(
          hash
        )}&type=${encodeURIComponent(type)}`;

        const response = await fetch(resource);
        const data = response.json();

        const text = data || "Errore";
        const markdown = marked.parse(text);

        markdownDisplay.innerHTML = markdown;
      } catch (error) {
        console.error("Error", error);
      }
    } else {
      alert("Selezionare un documento");
    }
  });
}
