import React from "react";
import Chatbot from "./chatbot/Chatbot";
import Info from "./Info";

const App = () => (
  <div className="container" >
    <div id="info">
  				<Info />
  	</div>
    <Chatbot />
  </div>
);

export default App;
