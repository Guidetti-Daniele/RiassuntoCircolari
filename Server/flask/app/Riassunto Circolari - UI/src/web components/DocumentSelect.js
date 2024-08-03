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

    .document-row {
      width: 100%;
      height: var(--document-select-row-height);
      padding: var(--document-select-row-vertical-padding)
        var(--document-select-row-horizontal-padding) !important;
      display: flex;
      align-items: center;
      gap: var(--document-select-row-gap);
      transition: background-color 0.5s;
      cursor: pointer;
    }

    .document-row:hover {
      background-color: var(--document-select-row-background-hover);
    }

    .document-row.active {
      color: var(--document-select-active-row) !important;
      font-weight: bold;
    }

    .document-row .icon {
      height: calc(var(--document-select-row-height) * 0.8);
      flex-shrink: 0;
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
    icon: { type: String },
  };

  constructor() {
    super();

    this.value = "";
    this.icon = "";

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
          <object
            class="icon"
            type="image/svg+xml"
            data=${this.icon}
            ?hidden=${!this.icon}
          ></object>
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
