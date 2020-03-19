const express = require("express");
const bodyParser = require("body-parser");
const path = require("path");
const http = require("http")

const app = express();
const PORT = process.env.PORT || 5000;

const server = http.createServer(app);


const DIST_DIR = path.join(__dirname, '../dist');
const HTML_FILE = path.join(DIST_DIR, '/index.html');


//Routes

//----

app.use(express.static(DIST_DIR));

app.use(bodyParser.json());

app.get("/", (req, res) => {
    res.status(200).send(HTML_FILE)
})

app.get("/api", (req, res) => {
    res.send({ hello: "there" });
});


server.listen(PORT, () => {
    console.log(`server started at port ${PORT}`);
});