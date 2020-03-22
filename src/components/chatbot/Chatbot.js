import React,{Component} from 'react';
import axios from "axios";
import {Widget,addResponseMessage} from 'react-chat-widget';
import messageSound from '../../assets/open-ended.mp3';


import 'react-chat-widget/lib/styles.css'

class Chatbot extends Component{
    constructor(props) {
        super(props);
        this.state = {
            messages: [],
        };

        this.sound = new Audio(messageSound);

        //Setting the cookie using uuid
        // if (!cookies.get("userID")) {
        //     cookies.set("userID", uuid(), { path: "/" });
        // }

        //Binding event listeners
        // this.toggleBot = this.toggleBot.bind(this);
        // this._handleInputKeyPress = this._handleInputKeyPress.bind(this);
    }


    resolveAfterXSeconds(time) {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(time);
            }, time * 1000);
        });
    }

    async componentDidMount(){

        if (!this.state.welcomeSent) {
            await this.resolveAfterXSeconds(1.2);
            this.df_event_query("WELCOME_TO_SITE");
        }
        // addResponseMessage("Welcome ");
    }


    async df_text_query(text){

        await axios.post("/api/df_text_query",{
            text
        }).then((response)=>{
            console.log(response)
            addResponseMessage(response.data)
        }).catch(err=>{
            console.log(err)
        })

        this.sound.play();
        
    }


    async df_event_query(event){
        await axios.get("/api/hello")
        .then((response)=>{
            console.log(response)
            addResponseMessage(response.data)
        }).catch(err=>{
            console.log(err)
        })


        this.sound.play()
    }


handleNewUserMessage=(newMessage)=>{

    this.df_text_query(newMessage)

    // addResponseMessage(res.toString());
}

    render(){
        return (
            <div>
                <Widget
                    handleNewUserMessage={this.handleNewUserMessage}
                />
            </div>
        )
    }
}

export default Chatbot; 