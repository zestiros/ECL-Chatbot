import React, { Component } from "react";
import axios from "axios";
import {
  Widget,
  addResponseMessage,
  renderCustomComponent,
  toggleMsgLoader,
  toggleWidget
} from "react-chat-widget";
import messageSound from "../../assets/open-ended.mp3";
import logo from "../../assets/bot.png";
import Satisfaction from "./Satisfaction";

import "react-chat-widget/lib/styles.css";

class Chatbot extends Component {
  constructor(props) {
    super(props);
    this.state = {
      notif: 0
    };

    this.sound = new Audio(messageSound);
  }

  resolveAfterXSeconds(time) {
    return new Promise(resolve => {
      setTimeout(() => {
        resolve(time);
      }, time * 1000);
    });
  }

  async componentDidMount() {
    if (!this.state.welcomeSent) {
      await this.resolveAfterXSeconds(1.2);
      this.hello();
    }
  }

  async df_text_query(text) {
    toggleMsgLoader();
    let model = "g";
    await axios
      .post("/api/df_text_query", {
        text,
        model
      })
      .then(response => {
        console.log(response);
        toggleMsgLoader();
        addResponseMessage(response.data);
        toggleMsgLoader();
        setTimeout(() => {
          toggleMsgLoader();
          addResponseMessage("êtes-vous satisfait de cette réponse?");
          renderCustomComponent(Satisfaction);
        }, 1500);
      })
      .catch(err => {
        console.log(err);
      });

    this.sound.play();
  }

  async hello() {
    toggleMsgLoader();
    await axios
      .get("/api/hello")
      .then(response => {
        console.log(response);
        toggleMsgLoader();
        addResponseMessage(response.data);
      })
      .catch(err => {
        console.log(err);
      });

    this.sound.play();
  }

  handleNewUserMessage = newMessage => {
    this.df_text_query(newMessage);
  };

  render() {
    return (
      <div>
        <Widget
          handleNewUserMessage={this.handleNewUserMessage}
          profileAvatar={logo}
          title="ECL Chatbot"
          subtitle=" "
          senderPlaceHolder="taper un message..."
          badge={this.state.notif}
        />
      </div>
    );
  }
}

export default Chatbot;
