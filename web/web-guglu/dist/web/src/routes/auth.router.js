const express = require("express");
const router = express.Router();
const db = require("../lib/db");

router.get("/login", (req, res) => {
	res.render("login");
})

router.post("/login", (req, res) => {
	const { username, password } = req.body;

	if (!username || !password) {
		return res.status(400).send("No username or password provided.");
	}

	const user = db.login(username, password);
	console.log(user);

	if (!user) {
		return res.status(403).send("Invalid credentials");
	}

	req.session.authenticated = true;
	req.session.username = user.username;

	return res.redirect("/home");
})

router.get('/register', (req, res) => {
	res.render("register");
})

router.post("/register", (req, res) => {
	const { username, password } = req.body;

	if (!username || !password) {
		return res.status(400).send("No username or password provided.");
	}

	const registered = db.register(username, password);
	
	if (!registered) {
		return res.status(403).send("User already registered.");
	}

	return res.redirect("/login");
})

router.get('/logout', (req, res) => {
	if (req.session) {
        req.session = null;
    }

	return res.redirect('/');
});

module.exports = router;
