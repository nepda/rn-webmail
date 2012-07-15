import sys

cfg_index_name = "index"

def main(conn, data):
	print "\r\n\r\n- - - - request for nepdaPy server - - - - - - - - - - - - - - "
	
	request = parseHeader(data)
	#print request['resource']
	
	resource = request['resource'][1:]
	
	if request['resource'] == "/" :
		resource = cfg_index_name
	
	try:
		mod = __import__("resource_" + resource)
		reload(mod)
		try:
			mod.main(conn, request)
		except:
			print "Unexpected error:", sys.exc_info()
	except:
		print "Unexpected error:", sys.exc_info()[0]
		conn.send("HTTP/1.0 404 OK\r\n")
		conn.send("Content-Type: text/html; charset=utf8\r\n")
		conn.send("\r\n")
		conn.send("<h1>404 Resource not found</h1>")
	print "\r\n\r\n- - - - request end : nepdaPy server - - - - - - - - - - - - - "

def parseHeader(data):
	#print "srv.parseHeader hat folgende Daten:\n"
	#print data
	
	header_and_body = data.split("\r\n\r\n")
	
	http_header = header_and_body[0]
	#http_body = header_and_body[1]
	
	header_lines = http_header.split("\r\n")
	
	h_first_line = header_lines[0]
	
	space_parts = h_first_line.split(" ")
	
	if len(space_parts) != 3 :
		print "kein gueltige http anfrage"
		return
	
	http_method = space_parts[0]
	http_request_file = space_parts[1]
	
	http_protocol = space_parts[2].split("/")[0]
	http_version = space_parts[2].split("/")[1]
	
	print "HTTP-Protcol: %s"%http_protocol
	print "HTTP-Version: %s"%http_version
	print "HTTP-Method: %s"%http_method
	print "HTTP-Req.-File: %s"%http_request_file
	
	request = {"protocol":http_protocol, "version":http_version, "method":http_method, "resource":http_request_file}
	return request

def status():
	return "ok"
