import {
  LitElement,
  html,
  css,
} from "https://cdn.jsdelivr.net/npm/lit@3.1.4/+esm";

import {
  ref,
  createRef,
} from "https://cdn.jsdelivr.net/npm/lit-html@3.1.4/directives/ref.js";

import { classMap } from "https://cdn.jsdelivr.net/npm/lit-html@3.1.4/directives/class-map.js";

export class DocumentSelect extends LitElement {
  static styles = css`
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      color: var(--document-select-color);
    }

    .wrapper {
      width: 100%;
      height: 100%;
      border-radius: var(--document-select-border-radius);
      background-color: var(--document-select-background);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
    }

    .wrapper.empty {
      padding: var(--document-select-empty-padding) 0;
      justify-content: center;
      align-items: center;
      background-color: var(--document-select-empty-background);
    }

    .wrapper.empty slot {
      color: var(--document-select-empty-text);
    }

    ::slotted(option) {
      width: 100%;
      padding: var(--document-select-option-vertical-padding)
        var(--document-select-option-horizontal-padding) !important;
      display: flex;
      align-items: center;
      gap: 2px;
      transition: background-color 0.5s;
      cursor: pointer;

      /* display: block;
      white-space: nowrap;
      overflow-x: hidden;
      text-overflow: ellipsis;
      transition: all 0.2s;
     */
    }

    ::slotted(option:hover) {
      background-color: var(--document-select-option-hover);
    }

    ::slotted(option.selected) {
      color: var(--document-select-active-color) !important;
      font-weight: bold;
    }
    /* .document-row:hover .document-description {
      display: table;
      white-space: wrap;
    }

    .document-row:hover .document-description::before {
      display: table-cell;
      border-left: 10px solid transparent;
      border-right: 10px solid transparent;
    } */
  `;

  static properties = {
    value: { type: String },
  };

  constructor() {
    super();

    this.value = "";

    // Refs
    this.slotRef = createRef();
  }

  // CLASS METHODS

  styleSelectedOption(event) {
    const clicked = event.target;

    if (clicked) {
      const options = this.slotRef.value.assignedElements();

      for (let option of options) {
        if (option.classList.contains("selected"))
          option.classList.remove("selected");
      }

      clicked.classList.add("selected");
    }
  }

  setValue(event) {
    this.styleSelectedOption(event);

    this.value = event.target.value;
    this.dispatchEvent(new Event("change"));
  }

  // ----------------------------------------

  render() {
    return html`
      <div
        class="wrapper ${classMap({
          empty: this.shadowRoot.host.children.length === 0,
        })}"
      >
        <slot ${ref(this.slotRef)} @click=${this.setValue}
          >Nessuna circolare disponibile per i campi selezionati</slot
        >
      </div>
    `;
  }
}

customElements.define("document-select", DocumentSelect);
