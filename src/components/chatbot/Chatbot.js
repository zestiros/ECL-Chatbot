import React, { Component } from "react";
import axios from "axios";
import {
  Widget,
  addResponseMessage,
  renderCustomComponent,
  toggleMsgLoader
} from "react-chat-widget";
import messageSound from "../../assets/open-ended.mp3";
import logo from "../../assets/bot.png";
import Satisfaction from "./Satisfaction";

import "react-chat-widget/lib/styles.css";

class Chatbot extends Component {
  constructor(props) {
    super(props);
    this.state = {
      messages: []
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
    // addResponseMessage("Welcome ");
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
          addResponseMessage("êtes-vous satisfait de cette réponse?");
          toggleMsgLoader();
        }, 1500);
        renderCustomComponent(Satisfaction);
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
          title="Chatbot"
          subtitle=" "
          senderPlaceHolder="taper un message..."
        />
      </div>
    );
  }
}

export default Chatbot;
