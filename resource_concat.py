import srv

def main(conn, request):
	srv.status200(conn, request)
	
	html = "Concat: "
	
	if "a" in request["params"]:
		html += request["params"]["a"] + " "
	if "b" in request["params"]:
		html += request["params"]["b"] + " "
		
	conn.send(html)