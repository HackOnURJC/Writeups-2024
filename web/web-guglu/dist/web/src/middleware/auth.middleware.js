verify = (req, res, next) => {
	const isAuthenticated = req.session.authenticated;

	if (isAuthenticated === true) {
		next();
	} else {
		return res.status(403).send({
			message: "You are not logged in!",
		});
	}

}

module.exports = {
	verify,
};
