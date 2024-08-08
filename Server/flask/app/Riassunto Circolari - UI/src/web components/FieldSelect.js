import {
  LitElement,
  html,
  css,
} from "https://cdn.jsdelivr.net/npm/lit@3.1.4/+esm";

import {
  ref,
  createRef,
} from "https://cdn.jsdelivr.net/npm/lit-html@3.1.4/directives/ref.js";

import { when } from "https://cdn.jsdelivr.net/npm/lit-html@3.1.4/directives/when.js";

import { classMap } from "https://cdn.jsdelivr.net/npm/lit-html@3.1.4/directives/class-map.js";

export class FieldSelect extends LitElement {
  static styles = css`
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      color: var(--field-select-text);
    }

    ::-webkit-scrollbar {
      width: var(--field-select-scrollbar-width);
    }

    ::-webkit-scrollbar-thumb {
      background: var(--field-select-scrollbar-thumb-background);
      border-radius: var(--field-select-scrollbar-border-radius);
    }

    ::-webkit-scrollbar-track {
      background: var(--field-select-scrollbar-track-background);
    }

    .wrapper {
      position: relative;
      width: 100%;
      height: 100%;
    }

    .current-option {
      width: 100%;
      height: 100%;
      padding: var(--field-select-vertical-padding)
        var(--field-select-horizontal-padding);
      border-radius: var(--field-select-border-radius);
      background-color: var(--field-select-background);
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: background-color 0.5s;
      cursor: pointer;
    }

    .current-option:hover {
      background: var(--field-select-background-on-hover);
    }

    .arrow {
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-top: 6px solid currentColor;
      transition: rotate 0.5s;
    }

    .menu {
      position: absolute;
      transform-origin: top;
      width: 100%;
      border-radius: var(--field-select-border-radius);
      overflow-y: auto;
      background: var(--field-select-background);
      z-index: 10;

      max-height: 0px;
      transition: max-height 0.2s;
    }

    ::slotted(option) {
      display: flex;
      align-items: center;
      min-height: var(--field-select-option-height);
      padding: var(--field-select-option-vertical-padding)
        var(--field-select-option-horizontal-padding) !important;
      color: var(--field-select-text) !important;
      transition: background-color 0.5s;
      cursor: pointer;
    }

    ::slotted(option:hover) {
      background-color: var(--field-select-option-background-on-hover);
    }

    /* When the FieldSelect is opened */

    .open .menu {
      max-height: var(--menu-max-height);
      box-shadow: 0 4px 8px 1px black;
    }

    .open .current-option {
      border: 1px solid var(--field-select-border-on-focus);
    }

    .open .arrow {
      rotate: 180deg;
    }
  `;

  static properties = {
    name: { type: String },
    valueTuple: { type: Array < String > 2 },
    isOpened: { type: Boolean },
  };

  constructor() {
    super();

    this.maxElementsInView = 7; // After this number of options will be compare a scrollbar
    this.name = ""; // Name of the field select if not provided the component won't be rendered
    this.valueTuple = []; // Tuple of 2 elements representing the selected option: the first value is the option text, the second is the option value
    this.isOpened = false; // Flag that indicates if the option menu is opened

    // Refs
    this.menuRef = createRef();
  }

  connectedCallback() {
    super.connectedCallback();

    document.addEventListener("click", (event) =>
      this.handleClick.apply(this, [event])
    );
  }

  disconnectedCallback() {
    super.disconnectedCallback();

    document.removeEventListener("click", (event) =>
      this.handleClick.apply(this, [event])
    );
  }

  // GETTERS & SETTERS

  get value() {
    return this.valueTuple[0];
  }

  set value(v) {
    this.valueTuple = [this.valueTuple[0], v];
  }

  // ----------------------------------------

  // CLASS METHODS:

  handleClick(event) {
    // Toggling the select when the user clicks on it
    const wasComponentClicked = this.toggleSelect(event);

    if (wasComponentClicked) return;

    // Closing the select if it's opened and the user clicks outside of it
    this.closeIfClickingOutside(event);
  }

  // return true if the component has been opened, false otherwise
  toggleSelect(event) {
    const clicked = event.composedPath()[0];

    if (clicked.closest(".current-option") && event.target.name === this.name) {
      this.isOpened = !this.isOpened;
      return true;
    }

    return false;
  }

  closeIfClickingOutside(event) {
    if (!this.isOpened) return;

    const menu = this.menuRef.value;
    const menuDimensions = menu.getBoundingClientRect();

    if (
      event.clientX < menuDimensions.left ||
      event.clientX > menuDimensions.right ||
      event.clientY < menuDimensions.top ||
      event.clientY > menuDimensions.bottom
    )
      this.isOpened = false;
  }

  handleSlotChange() {
    // Setting the max-height of the menu according to maxElementsInView
    this.setSlotMaxHeight();
  }

  setSlotMaxHeight() {
    const host = this.shadowRoot.host;

    const maxHeight = Array.from(host.children)
      .slice(0, this.maxElementsInView)
      .reduce((height, currentChild) => {
        const childHeight = currentChild.getBoundingClientRect().height;
        return height + childHeight;
      }, 0);

    const menuElement = this.menuRef.value;
    menuElement.style = `--menu-max-height: ${maxHeight}px`;
  }

  setValue(event) {
    this.valueTuple = [event.target.innerText, event.target.value];
    this.isOpened = false;

    this.dispatchEvent(new Event("change"));
  }

  // ----------------------------------------

  render() {
    return html`
      ${when(
        this.name,
        () => html`
          <main class="wrapper ${classMap({ open: this.isOpened })}">
            <section class="current-option">
              <span>${this.valueTuple[0] || this.name}</span>
              <div class="arrow"></div>
            </section>

            <section class="menu" ${ref(this.menuRef)}>
              <slot
                @slotchange=${this.handleSlotChange}
                @click=${this.setValue}
              >
                Error no option provided!
              </slot>
            </section>
          </main>
        `
      )}
    `;
  }
}

customElements.define("field-select", FieldSelect);
