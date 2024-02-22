# web-SevereTortureTo{{Creator}}

# Difficuty

easy

# Details

There is a golang application that is vulnerable to SSTI. You can check it by doing `{{.}}`

# Solve

First discover its gofiber

`{{printf '%#v' .}}`

After that, you can find by yourself a way to get arbitrary file read (did this and felt like a dumbass after finding out the following), or search in google `Golang SSTI`, which will result in [this post](https://payatu.com/blog/ssti-in-golang/) that explains you how to get arbitrary read.

```
{{ .Request.Response.SendFile "/flag.txt" }} {{ .Request.Response.Body }}
```
