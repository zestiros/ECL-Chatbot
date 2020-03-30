import React, { Component } from "react";


class DFile extends Component {
  constructor(props) {
    super(props);
  }



  render() {
    return (
     <div className="rcw-snippet">
       <h5 className="rcw-snippet-title">{this.props.title}</h5>
       <div className="rcw-snippet-details">
       <a href={this.props.value} target="_blank" className="rcw-link">ouvrir dans un nouvel onglet
       </a>
       
       </div>
     </div>
    );
  }
}

export default DFile;
