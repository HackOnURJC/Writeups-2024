package main

import (
    "log"
    "os"
    "io"
    "regexp"

    "github.com/gofiber/fiber/v2"
    "github.com/gofiber/template/html/v2"
)

const NotePath = "views/note.html"
const SamplePath = "views/sample.html"

func index(c *fiber.Ctx) error {
    return c.Render("index", fiber.Map{
	"Request": c,
    })
}

func add_note(c *fiber.Ctx) error {

    note := c.Body()

    match, err := regexp.MatchString("Shutdown", string(note[:]));
    if err == nil && match == true {
	return c.SendString("You are not shutting down anything today.");
    }

    source, err := os.Open(SamplePath);
    if err != nil {
	log.Println(err);
    }
    defer source.Close();

    dest, err := os.Create(NotePath);
    if err != nil {
	log.Println(err);
    }

    defer dest.Close();
    _, err = io.Copy(dest, source);
    if err != nil {
	log.Println(err);
    }

    f, err := os.OpenFile(NotePath,
	os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
	log.Println(err)
    }
    defer f.Close()
    if _, err := f.Write(note); err != nil {
	log.Println(err)
    }

    return c.Redirect("/note");
}

func view_note(c *fiber.Ctx) error {
    return c.Render("note", fiber.Map{
	"Title": "This is how your note was created",
	"Request": c,
    })
}

func main() {

    engine := html.New("./views", ".html")
    engine.Reload(true)

    app := fiber.New(fiber.Config {
	Views: engine,
    })

    app.Static("/static", "./public");

    app.Get("/", index)
    app.Post("/add-note", add_note)
    app.Get("/note", view_note)

    log.Fatal(app.Listen(":3000"))

}
