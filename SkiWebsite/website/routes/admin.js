var express = require('express');
var router = express.Router();
var pg = require('pg');
var escapePg = require('pg-escape');

var skiConfig = {
  host: 'localhost',
  user: 'postgres',
  database: 'ski',
  password: 'password',
  port: 5433,
  max: 10, // max number of clients in the pool
  idleTimeoutMillis: 30000, // how long a client is allowed to remain idle before being closed
};

var skiPool = new pg.Pool(skiConfig);

skiPool.on('error', function (err, client) {
  console.error('idle client error', err.message, err.stack)
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('admin', {});
});

module.exports = router;
