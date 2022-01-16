var express = require('express');
var router = express.Router();
var pg = require('pg');
var escapePg = require('pg-escape');
var moment = require('moment');

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
  res.render('populate', {});
});

router.post('/', function(req, res, next) {
  var timeDifference = req.body.time;
  console.log(timeDifference);
  var number = req.body.number;
  console.log(number);
  if(timeDifference == '' || number == '') {
    console.log('timeDifference = null || number = null')
    res.render('populate', {});
  }
  else {
    var currentTime = moment()
    var startTime = currentTime.format('MM-DD-YYYY HH:mm:ss.SSS');
    var endTime = currentTime.add(timeDifference,'seconds').format('MM-DD-YYYY HH:mm:ss.SSS');
    var netTime = '00:00:' + timeDifference

    skiPool.query(escapePg('INSERT INTO timer.times (start_time,end_time,net_time,number) VALUES (%L,%L,%L,%L)', startTime,endTime,netTime,number), function(err, result) {
      console.log(escapePg('INSERT INTO timer.times (start_time,end_time,net_time,number) VALUES (%L,%L,%L,%L)', startTime,endTime,netTime,number));
      res.render('populate', {});
    });
  }
});

module.exports = router;
