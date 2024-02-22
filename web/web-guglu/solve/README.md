# web-guglu

# explanation

In this website, there isn't any useful vulnerabilities (at least intended), but the way to leak the flag is the sort and pagination that there are at `/posts` and `/search`.

If you create 6 posts like `HackOn{a`, another 6 like `HackOn{b`, with fake images, pointing to a website you control, and from an external website, you do `window.open('chall.ctfd.io/?search=HackOn{b)')`, if you only receive 5 requests, the flag starts with `HackOn{a*`, as it was after `HackOn{a` and before `HackOn{b`