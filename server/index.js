const express = require("express");
const bodyParser = require("body-parser");
const path = require("path");
const http = require("http");
const { PythonShell } = require("python-shell");


const app = express();
const PORT = process.env.PORT || 5000;

const server = http.createServer(app);


const DIST_DIR = path.join(__dirname, '../dist');
const HTML_FILE = path.join(DIST_DIR, '/index.html');



//----

app.use(express.static(DIST_DIR));

app.use(bodyParser.json());

app.get("/", (req, res) => {
    res.status(200).send(HTML_FILE)
})

app.get("/api/hello", invokeChatbotWelcome);


app.post('/api/df_text_query', invokeChatbot);

app.get("/api/satisfied", () => {
    question = ""
})




/// chatbot code starts here


let generativeModelScript = path.join(__dirname, '.', '/py_files/generative_model/main.py')
let retrieveModelScript = path.join(__dirname, '.', '/py_files/retrieve_model/retrieve_model.py')
let question = ""

async function invokeChatbotWelcome(req, res) {
    console.log('welcome');
    var options = {
        mode: 'text',
        args: ["bonjour"]
    }

    await PythonShell.run(generativeModelScript, options, function(err, results) {
        if (err) console.log(err);
        res.send(results[0])
    });

}


async function invokeChatbot(req, res) {

    console.log("new message from client")



    if (req.body.model == "g") {
        question = req.body.text

        var options = {
            mode: 'text',
            args: [req.body.text]
        }

        await PythonShell.run(generativeModelScript, options, function(err, results) {
            if (err) console.log(err);

            console.log(results[0])
            res.send(results[0])
        })

    } else {

        console.log("retrieeeve" + question)

        let resp = []
        var options = {
            mode: 'text',
            args: [question]
        }

        await PythonShell.run(retrieveModelScript, options, function(err, results) {
            if (err) console.log(err);

            for (i = 0; i < 3; i++) {
                resp.push(results[i])
            }
            console.log(resp)
            res.send(resp)
        })
    }

    console.log("response sent!")
}





server.listen(PORT, () => {
    console.log(`server started at port ${PORT}`);
});