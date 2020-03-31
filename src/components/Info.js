import React from "react";

const Info = () => (
  <div>
    <h6>Bienvenue !</h6>{" "}
    <p id="desc">
      <br />
      Voici un Chatbot qui tentera de répondre aux questions que vous pouvez
      vous poser sur la scolarité ou sur l’associatif au sein de Centrale Lyon.
      <br />
      <br />
      <div id="descDiv">Voici quelques exemples de questions :</div>
      <br />
      * Qui est le responsable de l’UE Mathématiques ?<br />
      * Il y a combien de cours en mth tc1 ?<br />
      * Comment est évalué le cours d’analyse numérique ?<br />
      * Qui est le président du club Japon ?<br />
      * Quelle est l’adresse e-mail du trez pole logistique ?<br /><br/>

      Notre Chatbot n’a pas été suffisamment bien nourri en données pour générer
      des phrases efficacement, alors soyez indulgents.
      <br />
      Et dans les (nombreux) cas où sa réponse ne vous satisferait pas, dites-le
      lui, et il sera fera un plaisir de vous aiguiller à travers les ressources
      qu’il possède. Tel un moteur de recherche, il vous donnera en premier le
      lien le plus pertinent, avec la page qui vous intéresse.
      <br />
    </p>
    <h6>Bon Chat !</h6>
  </div>
);

export default Info;
