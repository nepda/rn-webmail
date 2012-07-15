
def main(conn, request):
	conn.send("HTTP/1.0 200 OK\r\n")
	conn.send("Content-Type: text/html; charset=utf8\r\n")
	conn.send("\r\n")
	conn.send("<h1>200 Resource found and loaded</h1>")
	print "resource found!"