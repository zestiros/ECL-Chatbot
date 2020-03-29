import React, { Component } from "react";
import axios from "axios"
import { addResponseMessage , addLinkSnippet } from "react-chat-widget";
import messageSound from "../../assets/open-ended.mp3";


class Satisfaction extends Component {
  constructor(props) {
    super(props);
    this.sound = new Audio(messageSound);

  }

  Oui() {
    addResponseMessage("Merci, Au revoir!");
  }

  Non() {
    this.df_text_query()
  }

  async df_text_query(text) {
    let model = "r";
    await axios
      .post("/api/df_text_query", {
        text,
        model
      })
      .then(response => {
        console.log(response);
        // addResponseMessage(response.data);
        for(let i=0;i<3;i++){
            var link={
                title : "file "+i,
                link : response.data[i],
                target:'_blank'
            }
            addLinkSnippet(link)
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
