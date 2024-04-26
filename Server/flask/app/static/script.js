document.addEventListener('DOMContentLoaded', function () {
    fetchDropdownData('recipient', '/get-destin', 'Destinatario');
    fetchDropdownData('class', '/get-class', 'Classe');
    fetchDropdownData('type', '/get-types', 'Tipo');
    setupDocumentDropdown();

    updateMarkdownDisplay();
    observeMarkdownChanges();
});

function updateMarkdownDisplay() {
    var markdownDisplay = document.getElementById('markdownDisplay');
    if (markdownDisplay.textContent.trim() === '') {
        markdownDisplay.classList.add('empty');
    } else {
        markdownDisplay.classList.remove('empty');
    }
}

function observeMarkdownChanges() {
    var markdownDisplay = document.getElementById('markdownDisplay');
    var observer = new MutationObserver(updateMarkdownDisplay);
    observer.observe(markdownDisplay, { childList: true, subtree: true, characterData: true });
}


function fetchDropdownData(elementId, endpoint, not_selected_text) {
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            const dropdown = document.getElementById(elementId);
            dropdown.innerHTML = '<option value="" disabled="" selected="">' + not_selected_text + '</option>'; // Clear existing options but keep the wise guide

            const separator = document.createElement('option');
            separator.disabled = true;
            dropdown.add(separator);

            data.forEach(item => {
                if (item !== "#separator#") {
                    const option = new Option(item, item);
                    dropdown.add(option);
                } else {
                    const separator = document.createElement('option');
                    separator.disabled = true;
                    dropdown.add(separator);
                }
            });
        })
        .catch(error => console.error('Error', error));
}

function fetchDocumentData(elementId, endpoint, data) {
    const queryString = Object.keys(data).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(data[key])).join('&');
    fetch(`${endpoint}?${queryString}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            const dropdown = document.getElementById(elementId);
            dropdown.innerHTML = '<option value="" disabled="" selected="">Documento</option>';

            const separator = document.createElement('option');
            separator.disabled = true;
            dropdown.add(separator);

            data.forEach(item => {
                const option = new Option(item[1], item[0]);
                dropdown.add(option);
            });
        })
        .catch(error => console.error('Errore', error));
}

function setupDocumentDropdown() {
    const triggers = ['type', 'recipient', 'class'];
    triggers.forEach(trigger => {
        document.getElementById(trigger).addEventListener('change', function () {
            const type = document.getElementById('type').value;
            const recipient = document.getElementById('recipient').value;
            const class_ = document.getElementById('class').value;

            if (type && recipient && class_) {
                const data = { dest: recipient, class: class_, type: type };
                fetchDocumentData('document', '/get-circ', data);
            }
        });
    });
}

document.getElementById('fetchTextButton').addEventListener('click', function () {
    const hash = document.getElementById('document').value;
    const type = document.getElementById('type').value;

    if (hash && type) {
        fetch(`/get-text?hash=${encodeURIComponent(hash)}&type=${encodeURIComponent(type)}`)
            .then(response => response.json())
            .then(data => {
                const text = data || 'Errore';
                const markdown = marked.parse(text);
                document.getElementById('markdownDisplay').innerHTML = markdown;
            })
            .catch(error => console.error('Errore', error));
    } else {
        alert('Selezionare un documento');
    }
});