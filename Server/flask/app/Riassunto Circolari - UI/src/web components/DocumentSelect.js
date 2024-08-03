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

    .wrapper:has(.empty-text) {
      background-color: var(--document-select-empty-background);
      padding: var(--document-select-empty-padding);
      justify-content: center;
      align-items: center;
    }

    .empty-text {
      color: var(--document-select-empty-text);
      text-align: center;
    }

    ::slotted(option) {
      width: 100%;
      padding: var(--document-select-option-vertical-padding)
        var(--document-select-option-horizontal-padding) !important;
      display: flex;
      align-items: center;
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

    img {
      display: block;
      height: 100%;
      aspect-ratio: 1;
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
    optionIcon: { type: String },
  };

  constructor() {
    super();

    this.value = "";
    this.optionIcon = "";

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

  isEmpty() {
    return this.shadowRoot.host.children.length === 0;
  }

  getEmptyText() {
    return html`<p class="empty-text">
      Nessuna circolare disponibile per i campi selezionati
    </p>`;
  }

  getDocumentRows() {
    return Array.from(this.shadowRoot.host.children)
      .filter((element) => element.tagName === "OPTION")
      .map((option) => {
        return html` <div class="document-row">
          <img src=${this.optionIcon} alt="icon" />
          <option value=${option.value}>${option.textContent}</option>
        </div>`;
      });
  }

  // ----------------------------------------

  render() {
    return html`
      <div class="wrapper">
        ${when(
          this.isEmpty(),
          () => this.getEmptyText(),
          () => this.getDocumentRows()
        )}
      </div>
    `;
  }
}

customElements.define("document-select", DocumentSelect);
