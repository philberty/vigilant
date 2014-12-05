/**
 * Created by redbrain on 04/12/2014.
 */
var express = require('express');
var router = express.Router();

var datastores = ['http://localhost:8080']

router.get('/', function(req, res) {
    res.send();
});

module.exports = router;
