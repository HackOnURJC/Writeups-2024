const express = require("express");
const router = express.Router();
const db = require("../lib/db");

router.get('/home', (req, res) => {
	res.render("home", {
		username : req.session.username,
	});
});

router.get('/post/:id', (req, res) => {
	const { id } = req.params;
	const user = req.session.username;

	const post = db.getPost(id, user);

	if (post === undefined) {
		return res.status(404).send("That post doesn't exist or you don't have access.");
	}
	console.log(`keys: ${Object.keys(post)}`)

	return res.render("post", {
		post : post,
	});
});

router.get('/posts', (req, res) => {
	const { page } = req.query;

	if (page === undefined) {
		return res.redirect('/posts?page=1')
	}

	const owner = req.session.username;

	const posts = db.getPosts(owner, page);

	return res.render('posts', {
		posts: posts,
	});
});

router.post('/add-post', (req, res) => {
	let { title, content, logo } = req.body;
	const creator = req.session.username;

	title = title.length <= 256
		? title
		: title.substring(0, 256);
	
	content = content.length <= 1024
		? content
		: content.substring(0, 1024);		

	const id = db.addPost(title, content, logo, creator)["lastInsertRowid"];

	return res.redirect(`/post/${id}`);
});

router.get('/search', (req, res) => {
	let query = req.query["query"] || '';
	let creator = req.session.username;
	let page = req.query["page"] || 1;

	const posts = db.searchPosts(query, creator, page);
	
	return res.render("posts", {
		posts: posts,
	});
})

module.exports = router;
