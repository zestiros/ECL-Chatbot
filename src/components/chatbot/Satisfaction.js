import React, { Component } from "react";
import axios from "axios";
import {
  addResponseMessage,
  renderCustomComponent,
  toggleMsgLoader
} from "react-chat-widget";
import messageSound from "../../assets/open-ended.mp3";
import DFile from "./DFile";

class Satisfaction extends Component {
  constructor(props) {
    super(props);
    this.sound = new Audio(messageSound);
  }

  async Oui() {
    toggleMsgLoader();
    setTimeout(()=>{
      toggleMsgLoader();
      addResponseMessage("Merci, au revoir!")
    },1500)
    await axios.get("/api/satisfied");
  }

  Non() {
    this.df_text_query();
  }

  async df_text_query() {
    toggleMsgLoader();

    let model = "r";
    await axios
      .post("/api/df_text_query", {
        model
      })
      .then(response => {
        console.log(response);
        // addResponseMessage(response.data);
        for (let i = 0; i < 3; i++) {
          var link = {
            title: "Voir " + response.data[i].page,
            link: response.data[i].link,
            abstract : response.data[i].abstract
          };
          toggleMsgLoader();
          renderCustomComponent(DFile, { title: link.title, value: link.link , abstract : link.abstract });
        }
      })
      .catch(err => {
        console.log(err);
      });

    this.sound.play();
  }

  render() {
    return (
      <div className="quick-buttons-container">
        <ul className="quick-buttons">
          <li className="quick-list-button">
            <button className="quick-button" onClick={() => this.Oui()}>
              Oui
            </button>
          </li>
          <li className="quick-list-button">
            <button className="quick-button" onClick={() => this.Non()}>
              Non
            </button>
          </li>
        </ul>
      </div>
    );
  }
}

export default Satisfaction;
