const { isAuth } = require('../middleware');

module.exports = function(app) {
	app.use("/", require('./auth.router'));
	app.use("/", [isAuth.verify], require('./post.router'));
};
