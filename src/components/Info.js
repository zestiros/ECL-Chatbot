import React from 'react';

import bot from "../assets/bot.png"

const Info = () => (
	<div className="card">
		<div className="card-image" style={{heigth: "150px"}}>
          <img src={bot} alt="bot"/>
          <span className="card-title">Hellooo!</span>
        </div>
        <div className="card-content">
          <p>
          ecl chatbot
          </p>
        </div>
	</div>
);

export default Info;