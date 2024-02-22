import http.server
import ssl

# openssl req -new -x509 -key priv.pem -out server.pem -days 365 -nodes

server_address = ('0.0.0.0', 4444)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
ctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
ctx.maximum_version = ssl.TLSVersion.TLSv1_2
ctx.set_ciphers('AES256-GCM-SHA384')
ctx.load_cert_chain(certfile="server.pem", keyfile="../priv.pem")
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()