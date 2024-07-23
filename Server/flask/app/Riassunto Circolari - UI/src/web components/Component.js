import {
  LitElement,
  html,
  css,
} from "https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js";

export class MyElement extends LitElement {
  static properties = {
    count: {},
  };

  static styles = css`
    button {
      background-color: red;
    }
  `;

  constructor() {
    super();
    this.count = 0;
  }

  handleClick() {
    console.log("ciao");
    this.count = this.count + 1;
  }

  render() {
    return html`
      <button @click=${() => this.handleClick()}>Clicked ${this.count}</button>
    `;
  }
}

customElements.define("my-element", MyElement);
