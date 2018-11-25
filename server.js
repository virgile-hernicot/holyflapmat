var http = require('http');
var url = require('url');
var fs = require('fs');
var express = require('express');
const shell = require('shelljs');
var app = express();


app.use(express.json());

app.get('/index.html', function (req, res) {
  var q = url.parse(req.url, true);
  var filename = "." + q.pathname;
  fs.readFile(filename, function(err, data) {
    if (err) {
      res.writeHead(404, {'Content-Type': 'text/html'});
      return res.end("404 Not Found");
    }
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(data);
    return res.end();
  });
});

app.get('/run', function (req,res){
  var json = {long: '123',lat: '123'};
  fs.writeFile('batch.json', JSON.stringify(json), 'utf8', function(err,data){
    shell.exec('../run.sh');
    return res.end('running');
  });
});

app.post('/compute', function(request, response){
    console.log(request.body);
    var json = {"users": request.body};
    fs.writeFile('./examples/input.test', JSON.stringify(json), 'utf8', function(err,data){
        shell.exec('./run.sh');
    });     // your JSON
    setTimeout(function() {
        fs.readFile('final_infos.json', function(err, data) {
            if (err) {
                res.writeHead(404, {'Content-Type': 'text/html'});
                return res.end("404 Not Found");
            }
            response.setHeader('Content-Type', 'application/json');
            response.send(JSON.parse(data));    // echo the result back
            return response.end();
        });
    }, 30000);

});

app.post('/results', function(request, response){
    console.log(request.body);
    response.writeHead(200, {'Content-Type': 'text/html'});
    return response.end("done");
});

app.listen(3000);
