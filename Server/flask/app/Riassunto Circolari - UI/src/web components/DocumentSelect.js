import {
  LitElement,
  html,
  css,
} from "https://cdn.jsdelivr.net/npm/lit@3.1.4/+esm";

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
      padding: var(--document-select-vertical-padding)
        var(--document-select-horizontal-padding);
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

    /* ::slotted(option) {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      padding: var(--document-select-option-vertical-padding)
        var(--document-select-option-horizontal-padding);
      gap: 2px;
      transition: background-color 0.5s;
      cursor: pointer;

      display: block;
      white-space: nowrap;
      overflow-x: hidden;
      text-overflow: ellipsis;
      transition: all 0.2s;
      user-select: none;
    }

    ::slotted(option:hover) {
      background-color: var(--document-select-option-hover);
    }

    ::slotted(option:not(:last-child)) {
      border-bottom: 1px solid var(--document-select-option-line);
    }

    ::slotted(option.selected) {
      color: var(--document-select-active-color);
      font-weight: bold;
    }

    ::slotted(option)::before {
      content: "\f1c1";
      font-family: FontAwesome;
      font-size: 18pt;
      margin: 0px 10px;
    } */

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

  constructor() {
    super();
  }

  render() {
    return html`
      <div
        class="wrapper ${classMap({
          empty: this.shadowRoot.host.children.length === 0,
        })}"
      >
        <slot>Nessuna circolare disponibile per i campi selezionati</slot>
      </div>
    `;
  }
}

customElements.define("document-select", DocumentSelect);
