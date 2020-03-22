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


//Routes

//----

app.use(express.static(DIST_DIR));

app.use(bodyParser.json());

app.get("/", (req, res) => {
    res.status(200).send(HTML_FILE)
})

app.get("/api/hello", invokeChatbotHi);


app.get('/ecl_nlp', (req, res) => {

    var pythonScriptPath = './chatbot_ecl.py'


    pyshell = new PythonShell(pythonScriptPath)

    pyshell.on('message', function(message) {
        console.log(message)
    })

    pyshell.end(function(err) {
        if (err) {
            throw err;
        }
    })

    console.log("finished")

    //Importing node 'child-process' module to spawn a child process
    // const { spawn } = require('child_process');

    //the spawned python process which takes 2 args , the name of the python script to invoke and the query param msg="hi"

    // var process = spawn('python', [
    //     "./chatbot_ecl.py", "combien cours mth tc1 ?"
    // ]);

    // process.stdout.on('data', function(data) {
    //     console.log("hi")
    //     console.log(data)
    //     res.send(data.toString());
    // })

})




/// chatbot code starts here

function invokeChatbotHi(req, res) {
    console.log('welcome');

    var pythonScriptPath = '/home/Projects/projet_option/ecl_chatbot/server/chatbot_ecl.py'

    var pyshell = new PythonShell(pythonScriptPath)

    var options = {
        mode: 'text',
        args: ["combien cours mth tc1 ?"]
    }

    PythonShell.run(pythonScriptPath, options, function(err, results) {
        if (err) console.log(err);


        res.send(results[0])
    });

}


function invokeChatbot(req, res) {

    console.log(req)
        //Importing node 'child-process' module to spawn a child process
    var spawn = require("child_process").spawn;

    //the spawned python process which takes 2 args , the name of the python script to invoke and the query param msg="hi"

    var process = spawn('python', [
        "./chatbot_ecl.py " +
        req.query.msg
    ]);
}




server.listen(PORT, () => {
    console.log(`server started at port ${PORT}`);
});