var express = require('express');
var bodyParser = require('body-parser');

var app = express();
var urlencodedParser = bodyParser.urlencoded({})


app.post('/aboutus',urlencodeParser,function(req,res){
    console.log(req.body);
    res.render('aboutus',{qs:req.query});
});