var template = document.getElementById('my-template');

template.innerHTML = `
    <img><img>
    <h3></h3>
    <p></p>
 
    <style>
      h3 {
        margin: 0px;
        color: darkmagenta;
        font-size: 24px;
      }
      p {
        line-height: 150%;
      }
      img {
        width: 40px;
        border-radius: 99px;
        margin-bottom: 12px;
      }
    </style>
`;

class UserCard extends HTMLElement {
    constructor() {
      super();
      
      this.attachShadow({ mode: 'open' });
      this.shadowRoot.appendChild(template.content.cloneNode(true)); 
      
    //   this.shadowRoot.querySelector('img').src = this.getAttribute('avatar');
      this.shadowRoot.querySelector('h3').innerText = this.getAttribute('name');
      this.shadowRoot.querySelector('p').innerText = this.getAttribute('ram'); 
      this.shadowRoot.querySelector('p').innerText = this.getAttribute('rom'); 
      this.shadowRoot.querySelector('p').innerText = this.getAttribute('description'); 
      this.shadowRoot.querySelector('p').innerText = this.getAttribute('description'); 
    }; 
};

window.customElements.define('user-card', UserCard);
