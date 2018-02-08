var express = require('express');
var router = express.Router();

var fs = require('fs');
var papa = require('papaparse');

router.get('/', function (req, res) {
	fs.readFile('C:\\Users\\LiZimeng\\Desktop\\workspace\\contract\\web\\server\\routes\\data.csv', 'utf8', function (err, data) {
		data = papa.parse(data, {header:true}).data;
		for (var i=0; i<data.length; i++) {
			data[i].beta0 = Number(data[i].beta0);
			data[i].beta1 = Number(data[i].beta1);
			data[i].R2 = Number(data[i].R2);
		}
		res.writeHead(200, {'Access-Control-Allow-Origin': '*'});
		console.log(JSON.stringify(data));
		res.end(JSON.stringify(data));
	});
});

module.exports = router;