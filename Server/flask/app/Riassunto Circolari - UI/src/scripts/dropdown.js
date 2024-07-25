// const dropdowns = document.querySelectorAll(".dropdown");

// 1). Opening/Closing the dropdown

// function toggleDropdown(event) {
//   const clicked = !event.target.classList.contains("dropdown-option")
//     ? event.target.closest(".dropdown")
//     : null;
//   const dropdownOpened = document.querySelector(".dropdown.opened");

//   if (dropdownOpened && clicked) dropdownOpened.classList.remove("opened");

//   clicked?.classList.add("opened");
// }

// 1.1). Also closing the dropdown when the user clicks outside of it

// document.addEventListener("click", (event) => {
//   const dropdownOpened = document.querySelector(".dropdown.opened");

//   if (dropdownOpened === null) return;

//   const dropdownOpenedMenu = dropdownOpened.querySelector(".dropdown-menu");
//   const dropdownMenuDimensions = dropdownOpenedMenu.getBoundingClientRect();

//   if (
//     event.clientX < dropdownMenuDimensions.left ||
//     event.clientX > dropdownMenuDimensions.right ||
//     event.clientY < dropdownMenuDimensions.top ||
//     event.clientY > dropdownMenuDimensions.bottom
//   )
//     dropdownOpened.classList.remove("opened");
// });

// 2). Selecting options in simple select-like-dropdowns
function selectOption(event) {
  const dropdownOpened = document.querySelector(".dropdown.opened");
  const optionText = event.target.innerText;

  if (dropdownOpened) {
    const dropdownSelectedText = dropdownOpened?.querySelector(
      ".selected-option-text"
    );

    dropdownSelectedText.innerText = optionText;
    dropdownOpened.classList.remove("opened");
  }
}

// Setting the event listener

// dropdowns.forEach((dropdown) => {
//   dropdown.addEventListener("click", (event) => toggleDropdown(event));

//   if (dropdown.classList.contains("select")) {
//     // TO-DO: Evaluate if making different dropdowns
//     dropdown.querySelectorAll(".dropdown-option").forEach((option) => {
//       option.addEventListener("click", (event) => selectOption(event));
//     });
//   }
// });
