import {
  LitElement,
  html,
  css,
} from "https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js";

export class FieldSelect extends LitElement {
  static styles = css`
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    .dropdown {
      position: relative;
      width: 100%;
      height: 100%;
    }

    .dropdown-selected {
      width: 100%;
      height: 100%;
      padding: 1.5em;
      border-radius: 5px;
      background-color: var(--select-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: background-color 0.5s;
      cursor: pointer;
      user-select: none;
    }

    .dropdown-selected:hover {
      background: var(--select-color-hover);
    }

    .arrow {
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-top: 6px solid currentColor;
      transition: rotate 0.5s;
    }

    .dropdown-menu {
      position: absolute;
      top: 50px;
      left: 0px;
      width: 100%;
      border-radius: 5px;
      background: var(--select-color);
      transform: translateY(-50px);
      opacity: 0;
      visibility: hidden;
      transition: transform, opacity, 0.5s;
      z-index: 10;
    }

    ::slotted(option) {
      height: 30px;
      padding: 1.2em 0.8em;
      display: flex;
      align-items: center;
      cursor: pointer;
      transition: background-color 0.5s;
      user-select: none;
    }

    ::slotted(option):hover {
      background-color: rgba(63, 63, 63, 0.747);
    }

    .dropdown-menu:has(::slotted(option):nth-child(8)) {
      max-height: 700%;
      overflow-y: scroll;
    }

    .dropdown .dropdown-menu {
      transform: translateY(0px);
      opacity: 1;
      visibility: visible;
      display: block;
    }

    .dropdown .dropdown-selected {
      border: 1px solid var(--green);
    }

    .dropdown .dropdown-selected .arrow {
      rotate: 180deg;
    }
  `;

  static properties = {
    name: {},
    value: {},
  };

  constructor() {
    super();

    this.name = "";
    this.value = "";
  }

  // Every slotted element which isn't an option will be removed
  firstUpdated() {
    const slot = this.renderRoot?.querySelector("slot");
    const slottedElements = slot.assignedElements();

    Array.from(slottedElements).forEach((slotted, index) => {
      if (slotted.tagName !== "OPTION") {
        const host = this.shadowRoot.host;
        const child = host.children[index];

        host.removeChild(child);
      }
    });
  }

  render() {
    return this.name
      ? html`
          <div class="dropdown">
            <div class="dropdown-selected">
              <span class="selected-option-text"
                >${this.value || this.name}</span
              >
              <div class="arrow"></div>
            </div>

            <div class="dropdown-menu">
              <slot> Error no option provided! </slot>
            </div>
          </div>
        `
      : html``;
  }
}

customElements.define("field-select", FieldSelect);
