const app = require('express')();
const server = require('http').createServer(app);
var cors = require('cors');
const shell = require('shelljs')
var port = 8000;


server.listen(port, () => console.log(`API server running on  ${port}!`))
app.use(cors())

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html')
})

app.get('/api/display/:status', (req, res) => {
    var status = req.params('status')
    if(status == 'on'){
        shell.exec('sudo systemctl start sensing.service')
        res.json({success:"display turned on for detection"})
    }else{
        shell.exec('sudo systemctl stop sensing.service')
        res.json({success:"display turned off for detection"})
    }
})