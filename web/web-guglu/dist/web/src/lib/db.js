'use strict'

const path = require('path');

const Database = require('better-sqlite3');
const db = new Database(path.resolve(__dirname, '/app/guglu.db'), { verbose : console.log });

function setUp() {
    db.exec(`
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    `);

    db.exec(`
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            logo TEXT NOT NULL,
            creator TEXT NOT NULL
        );
    `);

    const adminPwd = process.env.ADMIN_PWD || 'password';
    db.prepare(`	
        INSERT INTO users (id, username, password)
        VALUES (0, 'admin', ?);
    `).run(adminPwd);

    const Flag = process.env.FLAG || 'HackOn{fakeflag}';
    db.prepare(`
            INSERT INTO posts (id, title, content, logo, creator)
            VALUES (0, ?, 'Boring post, anyway, only I am reading it.',
            'https://cdn.vox-cdn.com/uploads/chorus_asset/file/22312759/rickroll_4k.jpg',
            'admin');
    `).run(Flag);
}

function register(username, password) {
    let stmt = db.prepare("SELECT username FROM users WHERE username = ?;");
    let user = stmt.get(username);
    if (user) return false;

    stmt = db.prepare("INSERT INTO users (username, password) VALUES (?, ?);");
    stmt.run(username, password);
    return true;
}

function login(username, password) {
    const stmt = db.prepare("SELECT username FROM users WHERE username = ? AND password = ?;");
    const user = stmt.get(username, password);
    return user;
}

function addPost(title, content, logo, creator) {
    const stmt = db.prepare("INSERT INTO posts (title, content, logo, creator) VALUES (?, ?, ?, ?);")
    const post_id = stmt.run(title, content, logo, creator);
    return post_id;
}

function getPost(id, creator) {
    const stmt = db.prepare("SELECT title, content, logo FROM posts WHERE id = ? AND creator = ?;");
    return stmt.get(id, creator);
}

function getPosts(owner, page) {
    const offset = (page - 1) * 6;
    
    if (owner == "admin") {

        const stmt = db.prepare("SELECT id, title, content, logo FROM posts ORDER BY title LIMIT 6 OFFSET ?;");
        const posts = stmt.all(offset);
        return posts;

    } else {

        const stmt = db.prepare("SELECT id, title, content, logo FROM posts WHERE creator = ? ORDER BY title LIMIT 6 OFFSET ?;");
        const posts = stmt.all(owner, offset);
        return posts;

    }
}

function searchPosts(query, owner, page) {
    const offset = (page - 1) * 6;

    if (owner == "admin") {

        const stmt = db.prepare("SELECT id, title, content, logo FROM posts WHERE title LIKE ? ORDER BY title LIMIT 6 OFFSET ?;");
        const posts = stmt.all(`%${query}%`, offset);
        return posts;

    } else {
         
        const stmt = db.prepare("SELECT id, title, content, logo FROM posts WHERE title LIKE ? and creator = ? ORDER BY title LIMIT 6 OFFSET ?;");
        const posts = stmt.all(`%${query}%`, owner, offset);
        return posts;       

    }
}

module.exports = {
    setUp,
    register,
    login,
    addPost,
    getPost,
    getPosts,
    searchPosts
}
