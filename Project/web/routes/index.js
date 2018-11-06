var express = require('express');
var passport = require('passport');
var router = express.Router();
var mysql = require('mysql');
var dbconfig = require('../config/database');
var connection = mysql.createConnection(dbconfig.connection);

connection.connect(function (err) {
	if (err) {
		console.log('connecting error');
		return;
	}
	console.log('connecting gps table success');
});

router.get('/', function (req, res, next) {
	res.render('index', { title: 'Express' });
});

router.get('/login', function (req, res, next) {
	res.render('login.ejs', { message: req.flash('loginMessage') });
});

router.get('/signup', function (req, res) {
	res.render('signup.ejs', { message: req.flash('signupMessage') });
});

router.get('/home', isLoggedIn, function (req, res) {
	res.render('home.ejs', { suser: req.user });
});

router.post('/home', function (req, res, next) {
	var sql = {
		gpslat: req.body.gpslat,
		gpslng: req.body.gpslng,
		username: req.body.username
	};
	console.log(sql);

	//console.log(sql);
	connection.query('INSERT INTO gps SET ?', sql, function (err, rows) {
		console.log("insert success");
		if (err) {
			console.log(err);
		}
		res.setHeader('Content-Type', 'application/json');
	});
});

router.get('/history', isLoggedIn, function (req, res) {
	var data = "";
	var loc = "";
	var user = "";
	var user = req.query.user;
	console.log(user);
	if (user) {
		connection.query('SELECT * FROM gps WHERE username = ? ORDER BY id DESC', user, function (err, rows) {
			if (err) {
				console.log(err);
			}
			loc = rows;

			/*res.render('tracing.ejs', {data: data, suser: req.user, loc: loc, lat: lat, lng: lng});*/
		});
	}

	connection.query('SELECT * FROM account ', function (err, rows) {
		if (err) {
			console.log(err);
		}
		var data = rows;
		console.log(loc);
		res.render('history.ejs', { data: data, suser: req.user, user: user, loc: loc });

	});
});

router.get('/nearby', isLoggedIn, function (req, res) {
	var name = "";
	connection.query('SELECT * FROM account ', function (err, rows) {
		if (err) {
			console.log(err);
		}
		name = rows;

	});
	connection.query('SELECT * FROM gps', function (err, rows) {
		if (err) {
			console.log(err);
		}
		var data = rows;
		res.render('nearby.ejs', { data: data, suser: req.user, name: name });

	});
});

router.get('/tracing', isLoggedIn, function (req, res) {
	var data = "";
	var user = "";
	var user = req.query.user;
	var loc = "";
	var lat = "";
	var lng = "";
	console.log(user);
	if (user) {
		connection.query('SELECT * FROM gps WHERE username = ?', user, function (err, rows) {
			if (err) {
				console.log(err);
			}
			var loc = rows;
			console.log(rows[loc.length - 1].id);
			lat = rows[loc.length - 1].gpslat;
			lng = rows[loc.length - 1].gpslng;
			/*res.render('tracing.ejs', {data: data, suser: req.user, loc: loc, lat: lat, lng: lng});*/
		});
	}
	connection.query('SELECT * FROM account ', function (err, rows) {
		if (err) {
			console.log(err);
		}
		var data = rows;
		res.render('tracing.ejs', { data: data, suser: req.user, user: user, loc: loc, lat: lat, lng: lng });

	});

});

router.get('/sensor', isLoggedIn, function (req, res) {
	var sen = "";
	var user = "";
	var user = req.query.user;
	var max = "";
	var min = "";
	var avg = "";
	console.log(user);
	if (user) {
		connection.query('SELECT  MAX(temperature) FROM sensor WHERE DATE(date) = ?', user, function (err, rows) {
			if (err) {
				console.log(err);
			}
			tem = JSON.stringify(rows);
			num = tem.split(":")
			max = num[1].slice(0,num[1].length-2)
			console.log(max);
	
		});
		connection.query('SELECT  MIN(temperature) FROM sensor WHERE DATE(date) = ?', user, function (err, rows) {
			if (err) {
				console.log(err);
			}
			tem = JSON.stringify(rows);
			num = tem.split(":")
			min = num[1].slice(0,num[1].length-2)
			console.log(min);
	
		});
		connection.query('SELECT  AVG(temperature) FROM sensor WHERE DATE(date) = ?', user, function (err, rows) {
			if (err) {
				console.log(err);
			}
			tem = JSON.stringify(rows);
			num = tem.split(":")
			avg = num[1].slice(0,num[1].length-2)
			console.log(avg);
	
		});
		connection.query('SELECT * FROM sensor WHERE DATE(date) = ? ORDER BY id DESC', user, function (err, rows) {
			if (err) {
				console.log(err);
			}
			sen = rows;

			res.render('sensor.ejs', { suser: req.user, user: user, sen: sen, max: max, min: min, avg: avg });
		});
	}else{
		res.render('sensor.ejs', { suser: req.user, user: user, sen: sen, max: max,  min: min, avg: avg });
	}
});

router.get('/logout', function (req, res) {
	req.logout();
	res.redirect('/');
});

router.post('/signup', passport.authenticate('local-signup', {
	successRedirect: '/home',
	failureRedirect: '/signup',
	failureFlash: true,
}));

router.post('/login', passport.authenticate('local-login', {
	successRedirect: '/home',
	failureRedirect: '/login',
	failureFlash: true,
}));

module.exports = router;

function isLoggedIn(req, res, next) {
	if (req.isAuthenticated())
		return next();
	res.redirect('/');
}
