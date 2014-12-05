/**
 * Created by redbrain on 04/12/2014.
 */
var Client = require('node-rest-client').Client;
var express = require('express');
var router = express.Router();

var datastores = ['http://localhost:8080']
var client = new Client();

router.get('/state', function(req, res) {

    var resp = {
        'datastores': datastores,
        'hosts': 0,
        'processes': 0
    };

    for (var i in datastores) {
        var store = datastores[i];
        client.get(store + '/hosts/keys', function(data, response) {

            console.log(data)
        });
    }

    res.json(resp);
});

module.exports = router;
