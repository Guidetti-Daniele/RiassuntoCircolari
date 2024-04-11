function get_dest() {
    const xhttp = new XMLHttpRequest();

    xhttp.onload = function () {
        destins = JSON.parse(this.responseText);
        dropdownMenu = document.getElementById("dest-menu");
        dropdownMenu.innerHTML = "";

        set_menu(destins, dropdownMenu, "selected-dest");
    }

    xhttp.open("GET", "get-destin", true);
    xhttp.send();
}

function get_class() {
    const xhttp = new XMLHttpRequest();

    xhttp.onload = function () {
        destins = JSON.parse(this.responseText);
        dropdownMenu = document.getElementById("class-menu");
        dropdownMenu.innerHTML = "";

        set_menu(destins, dropdownMenu, "selected-class");
    }

    xhttp.open("GET", "get-class", true);
    xhttp.send();
}

function set_menu(values, dropdownMenu, x_id) {
    for (var x of values) {
        var newMenu = document.createElement("li");
        var newLink;

        if (x != "#separator#") {
            newLink = document.createElement("a");

            newLink.href = "#";

            (function (x, y) {
                newLink.addEventListener("click", function (event) {
                    if (this.getAttribute("href") === "#") {
                        event.preventDefault();
                        set_selected_x(x, y);
                    }
                });
            })(x, x_id);

            newLink.textContent = x;
        } else {
            newLink = document.createElement("li");
            newLink.role = "separator";
            newLink.className = "divider";
        }

        newMenu.appendChild(newLink);
        dropdownMenu.appendChild(newMenu);
    }
}

function set_selected_x(text, x) {
    textElement = document.getElementById(x);
    textElement.innerHTML = text;
}