var express = require('express');
var router = express.Router();

var mysql = require('mysql');
var util = require('util');
var ols = require('jStat').models.ols;

router.get('/', function(req, res) {
	var params = req.query;
	
	var conn = mysql.createConnection({
		host: '219.224.169.45',
		user: 'lizimeng',
		password: 'codegeass',
		database: 'market',
		charset: 'utf8',
	});
	
	conn.connect();
	
	var sql = util.format('select %s from contract_daily where vari=? and deli=? order by day asc', params.field);
	console.log(sql);
	conn.query(sql, [params.vari, params.deli], function (err, results) {
		var data;
		
		if (err || results.length===0) {
			data = null;
			
		} else {
			data = {};
			var series = new Array();
			for (var i=0; i<results.length; i++) {
				series.push(results[i][params.field]);
			}
			data.series = series;
			
			var X = new Array(), Y = new Array();
			for (var i=1; i<series.length; i++) {
				X.push([1, series[i-1]]);
				Y.push(series[i]);
			}
			var model = ols(Y, X);
			data.beta0 = model.coef[0];
			data.beta1 = model.coef[1];
			data.R2 = model.R2;
		}
		
		res.writeHead(200, {'Access-Control-Allow-Origin': '*'});
		conn.end();
	});
});

module.exports = router;
