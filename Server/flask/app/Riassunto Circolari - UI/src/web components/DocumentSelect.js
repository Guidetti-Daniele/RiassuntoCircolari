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
      min-height: var(--document-select-row-height);
      padding: var(--document-select-row-vertical-padding)
        var(--document-select-row-horizontal-padding) !important;
      display: flex;
      align-items: center;
      gap: var(--document-select-row-gap);
      transition: background-color, max-height, 0.5s;
      cursor: pointer;
    }

    .document-row:hover {
      background-color: var(--document-select-row-background-hover);
    }

    .document-row .icon {
      height: calc(var(--document-select-row-height) * 0.8);
      flex-shrink: 0;
      pointer-events: none;
    }

    .document-row option {
      white-space: nowrap;
      overflow-x: hidden;
      text-overflow: ellipsis;
    }

    .document-row:hover option {
      white-space: wrap;
    }

    .document-row.active option {
      color: var(--document-select-active-row);
      font-weight: bold;
    }
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

    // Coloring the icon of the active option with the active color USING THE FILL ATTRIBUTE of the SVG tag

    // 1). First removing the active color to the icon of the previous active option
    this.setIconColor(this.getNormalColor(), previousValue);

    // 2). Then apply the active color to the icon of the new active option
    this.setIconColor(this.getActiveColor(), value);

    this.dispatchEvent(new Event("change"));
  }

  getNormalColor() {
    return getComputedStyle(this.shadowRoot.host).getPropertyValue(
      "--document-select-color"
    );
  }

  getActiveColor() {
    return getComputedStyle(this.shadowRoot.host).getPropertyValue(
      "--document-select-active-row"
    );
  }

  getOptionByValue(value) {
    return this.renderRoot?.querySelector(
      `.document-row option[value="${value}"]`
    );
  }

  setIconColor(color, optionValue) {
    const option = this.getOptionByValue(optionValue);

    if (option) {
      const icon = option.parentElement.querySelector("object");

      icon
        .getSVGDocument()
        .getElementById(SVG_DOCUMENT_ICON_ID)
        .setAttribute("fill", color);
    }
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
