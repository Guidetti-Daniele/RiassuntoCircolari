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
      transform: translateY(-50%);
      width: 100%;
      border-radius: 5px;
      overflow-y: auto;
      background: var(--field-select-background);
      box-shadow: 0 4px 8px 1px black;
      opacity: 0;
      visibility: hidden;
      transition: transform, opacity, 0.5s;
      z-index: 10;
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

    .menu {
      transform: translateY(0px);
      opacity: 1;
      visibility: visible;
    }

    .current-option {
      border: 1px solid var(--green);
    }

    .arrow {
      rotate: 180deg;
    }
  `;

  static properties = {
    maxElementsInView: {},
    name: {},
    value: {},
  };

  constructor() {
    super();

    this.updatedSlot = false; // This flag is used to avoid to run the handleSlotChange method twice
    this.maxElementsInView = 7; // After this number of options will be compare a scrollbar
    this.name = ""; // name of the field
    this.value = ""; // the current of the selected option
  }

  handleSlotChange() {
    if (this.updatedSlot) {
      this.updatedSlot = false;
      return;
    }

    // Every slotted element which isn't an option will be removed
    const host = this.shadowRoot.host;
    const slot = this.renderRoot?.querySelector("slot");
    const slottedElements = slot.assignedElements();

    Array.from(slottedElements).forEach((slotted, index) => {
      if (slotted.tagName !== "OPTION") {
        const child = host.children[index];

        // N.B: this operation causes the event @slotchange to be fired
        // so I set the flag updatedSlot to true to avoid to make this method running again.
        host.removeChild(child);
      }
    });

    this.updatedSlot = true;

    // Setting the max-height of the menu according to maxElementsInView
    const maxHeight = Array.from(host.children)
      .slice(-this.maxElementsInView)
      .reduce((height, currentChild) => {
        const childHeight = currentChild.getBoundingClientRect().height;
        return height + childHeight;
      }, 0);

    const menuElement = this.renderRoot?.querySelector(".menu");
    menuElement.style.maxHeight = `${maxHeight}px`;
  }

  render() {
    return this.name
      ? html`
          <div class="wrapper">
            <div class="current-option">
              <span>${this.value || this.name}</span>
              <div class="arrow"></div>
            </div>

            <div class="menu">
              <slot @slotchange=${this.handleSlotChange}>
                Error no option provided!
              </slot>
            </div>
          </div>
        `
      : html``;
  }
}

customElements.define("field-select", FieldSelect);
