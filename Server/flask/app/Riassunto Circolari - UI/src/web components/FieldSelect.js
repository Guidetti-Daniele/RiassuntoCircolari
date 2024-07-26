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
      color: var(--field-select-color);
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
      border-radius: 5px;
      background-color: var(--field-select-background);
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: background-color 0.5s;
      cursor: pointer;
      user-select: none;
    }

    .current-option:hover {
      background: var(--field-select-background-hover);
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
      border-radius: 5px;
      overflow-y: auto;
      background: var(--field-select-background);
      z-index: 10;

      max-height: 0px;
      transition: max-height 0.2s;
    }

    .menu::-webkit-scrollbar {
      width: var(--field-select-scrollbar-width);
    }

    .menu::-webkit-scrollbar-thumb {
      background: var(--field-select-scrollbar-thumb-background);
      border-radius: var(--field-select-scrollbar-border-radius);
    }

    .menu::-webkit-scrollbar-track {
      background: var(--field-select-scrollbar-track-background);
    }

    ::slotted(option) {
      display: flex;
      align-items: center;
      min-height: var(--field-select-option-min-height);
      padding: var(--field-select-option-vertical-padding)
        var(--field-select-option-horizontal-padding) !important;
      color: var(--field-select-color) !important;
      transition: background-color 0.5s;
      cursor: pointer;
      user-select: none;
    }

    ::slotted(option:hover) {
      background-color: var(--field-select-option-hover);
    }

    .open .menu {
      max-height: var(--menu-max-height);
      box-shadow: 0 4px 8px 1px black;
    }

    .open .current-option {
      border: 1px solid var(--field-select-focus-border-color);
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

    this.updatedSlot = false; // This flag is used to avoid to run the handleSlotChange method twice
    this.maxElementsInView = 7; // After this number of options will be compare a scrollbar
    this.name = ""; // Name of the field select
    this.valueTuple = []; // The selected option
    this.isOpened = false; // Flag that indicates if the option menu is opened

    // Refs
    this.menuRef = createRef();
    this.slotRef = createRef();
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
    // Avoiding to make the method running again after this.clearSlottedElements() or
    // other methods that changes the slot  are invoked
    if (this.updatedSlot) {
      this.updatedSlot = false;
      return;
    }

    // Every slotted element which isn't an option will be removed
    this.clearSlottedElements();

    // Setting the max-height of the menu according to maxElementsInView
    this.setSlotMaxHeight();
  }

  clearSlottedElements() {
    const host = this.shadowRoot.host;
    const slot = this.slotRef.value;
    const slottedElements = slot.assignedElements();

    Array.from(slottedElements).forEach((slotted, index) => {
      if (slotted.tagName !== "OPTION") {
        const child = host.children[index];

        // N.B: this operation causes the event @slotchange to be fired
        // so I set the flag updatedSlot to true to avoid to make this method running again.
        host.removeChild(child);
        this.updatedSlot = true;
      }
    });
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
          <div class="wrapper ${classMap({ open: this.isOpened })}">
            <div class="current-option">
              <span>${this.valueTuple[0] || this.name}</span>
              <div class="arrow"></div>
            </div>

            <div class="menu" ${ref(this.menuRef)}>
              <slot
                @slotchange=${this.handleSlotChange}
                @click=${this.setValue}
                ${ref(this.slotRef)}
              >
                Error no option provided!
              </slot>
            </div>
          </div>
        `
      )}
    `;
  }
}

customElements.define("field-select", FieldSelect);
