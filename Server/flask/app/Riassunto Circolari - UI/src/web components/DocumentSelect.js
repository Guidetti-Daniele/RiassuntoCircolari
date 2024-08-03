import {
  LitElement,
  html,
  css,
} from "https://cdn.jsdelivr.net/npm/lit@3.1.4/+esm";

import { when } from "https://cdn.jsdelivr.net/npm/lit-html@3.1.4/directives/when.js";

import { classMap } from "https://cdn.jsdelivr.net/npm/lit-html@3.1.4/directives/class-map.js";

// N.B: ASSERT TO ASSIGN THE SVG ID IN THE SVG CODE IF YOU WANT TO CHANGE THE ICON
const SVG_DOCUMENT_ICON_ID = "svg-id";
// -----------------------------------------------

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

    .document-row.active option {
      color: var(--document-select-active-row);
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
  }

  // CLASS METHODS

  setValue(value) {
    const previousValue = this.value;
    this.value = value;

    this.setIconActiveColor(previousValue, value); // Coloring the active icon USING THE FILL ATTRIBUTE of the SVG tag

    this.dispatchEvent(new Event("change"));
  }

  setIconActiveColor(previousValue, newValue) {
    const host = this.shadowRoot.host;
    const normalIconColor = getComputedStyle(host).getPropertyValue(
      "--document-select-color"
    );
    const activeIconColor = getComputedStyle(host).getPropertyValue(
      "--document-select-active-row"
    );

    // First removing the active color to the icon of the previous active option...
    const previousActiveOption = this.renderRoot?.querySelector(
      `.document-row option[value="${previousValue}"]`
    );

    if (previousActiveOption) {
      const previousIcon =
        previousActiveOption.parentElement.querySelector("object");

      previousIcon
        .getSVGDocument()
        .getElementById(SVG_DOCUMENT_ICON_ID)
        .setAttribute("fill", normalIconColor);
    }

    // ... then coloring the new active one
    const activeOption = this.renderRoot?.querySelector(
      `.document-row option[value="${newValue}"]`
    );
    const activeIcon = activeOption.parentElement.querySelector("object");
    activeIcon
      .getSVGDocument()
      .getElementById(SVG_DOCUMENT_ICON_ID)
      .setAttribute("fill", activeIconColor);
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
        return html` <div
          class="document-row ${classMap({
            active: this.value === option.value,
          })}"
          @click=${() => this.setValue(option.value)}
        >
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
