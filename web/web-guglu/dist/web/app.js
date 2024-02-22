const express = require('express');
const cookieSession = require('cookie-session');
const bodyParser = require('body-parser')

const crypto = require('crypto');
const path = require('path')
const { setUp } = require('./src/lib/db');
setUp();

const port = process.env.PORT || 3000;
const app = express();

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, '/src/views'))
app.use(express.static('src/public'))

app.use(
	bodyParser.urlencoded({
		extended: true,
	}),

	cookieSession({
		secret: crypto.randomBytes(32).toString('hex'),
		cookie : {
			httpOnly: true,
			secure: false,
			maxAge: 1000 * 60 * 60 * 24,
		},
	}),
);

app.get('/', (req, res) => {
	if (req.session.authenticated) {
		return res.redirect('/home');
	} else {
		return res.render("index");
	}
})

require("./src/routes/routes")(app);

app.use('*', (req, res) => {
	res.status(404).send("This endpoint doesn't seem to exists.");
})

app.listen(port, () => {
	console.log(`[+] Web app running at port ${port}`);
})
