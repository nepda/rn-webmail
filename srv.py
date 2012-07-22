import sys

cfg_index_name = "index_html"

def main(conn, data):
	print "\r\n\r\n- - - - request for nepdaPy server - - - - - - - - - - - - - - "
	
	request = parseHeader(data)
	#print request['resource']
	
	resource = request['resource'][1:]
	
	if request['resource'] == "/" :
		resource = cfg_index_name
	
	try:
		mod = __import__("resource_" + resource.replace(".", "_"))
		reload(mod)
		try:
			mod.main(conn, request)
		except:
			print "Unexpected error:", sys.exc_info()
	except ImportError:
		print "The resource %s was not found"%request['resource']
		conn.send("HTTP/1.0 404 Not Found\r\n")
		conn.send("Content-Type: text/html; charset=utf8\r\n")
		conn.send("\r\n")
		conn.send("<h1>Not Found</h1><p>The requested URL %s was not found on this server</p>"%request['resource'])
	except:
		print "404 not found:", sys.exc_info()[0]
		conn.send("HTTP/1.0 500 OK\r\n")
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
	url_params = {} # dict
	
	# Wenn (ein) URL Parameter angegeben sind/ist ist dies eindeutig an dem Fragezeichen zu erkennen.
	# <string>.find(<string>) liefert die Position des gefunden zurueck, wenn nix gefunden wurde, wird -1 zurueckgeliefert
	# 
	# alle Weiteren Parameter werden durch ein & getrennt...
	if http_request_file.find("?") > 1:
		tmp = http_request_file.split("?")
		http_request_file = tmp[0]
		params = tmp[1] # hier muss noch geprueft werden, ob ein oder mehrere Parameter angegeben wurden.
		
		# Prueft, ob ein oder mehrere Parameter uebergeben wurden
		if params.find("&") > 0:
			params = params.split("&") # Inhalt von params koennte jetzt so was sein: params = ['a=val', 'b=other']
		else:
			params = [params]
			# params koennte so aussehen: params = ['a=val']
			
		print params
			
		for key_value_pair in params:
			if key_value_pair.find("=") > 0:
				key = key_value_pair.split("=")[0]
				value = key_value_pair.split("=")[1]
			else:
				key = key_value_pair
				value = None
				
			url_params[key] = value
	
	http_protocol = space_parts[2].split("/")[0]
	http_version = space_parts[2].split("/")[1]
	
	print "URL-Parameter: %s"%url_params
	print "HTTP-Protcol: %s"%http_protocol
	print "HTTP-Version: %s"%http_version
	print "HTTP-Method: %s"%http_method
	print "HTTP-Req.-File: %s"%http_request_file
	
	request = {"protocol":http_protocol, "version":http_version, "method":http_method, "resource":http_request_file, "params":url_params}
	return request

def status():
	return "ok"
