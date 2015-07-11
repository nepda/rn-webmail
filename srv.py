import sys, urllib

cfg_index_name = "/index_html" # legt die Standardresource fest (Datei: resource_index_html.py)

def main(conn, data):
	print "\r\n\r\n- - - - request for nepdaPy server 2 - - - - - - - - - - - - - - "

	request = parseHeader(data) # sucht relevante infos aus dem Header
	#
	# Beispiel reuqest: http://localhost:5001/index.html?param1=value1&param2=val2
	# wuerde folgendes ergeben:
	# reuqest = {'resource': '/index.html', 'version': '1.1', 'protocol': 'HTTP', 'method': 'GET', 'params': {'param1': 'value1', 'param2': 'val2'}}


	resource = request['resource']

	# Wenn also keine Resource explizit angegeben wurde
	if resource == "/" :
		resource = cfg_index_name # standard Seite laden

	resource = resource[1:] # Resource ohne den anfangs Slash

	try:
		mod = __import__("resource_" + resource.replace(".", "_")) # Importiert die Datei "resource_<module_name>"
		reload(mod) # laedt die Datei neu, falls sie geaendert wurde (koennte man rausnehmen, wenn der Server komplett fertig geschrieben ist
		try:
			mod.main(conn, request)                      # ACHTUNG! Jede Resource MUSS die Funktion main(self, connection, request) anbieten. Dies ist der Einstiegspunkt
		except:
			print "Unexpected module error", sys.exc_info()
	except ImportError: # Wenn das Modul nicht gefunden wurde
		print "The resource %s was not found"%resource
		status404(conn, request)
	except:
		print "500 server error:", sys.exc_info()
		status500(conn, request)
	print "\r\n\r\n- - - - request end : nepdaPy server - - - - - - - - - - - - - "

def parseHeader(data):
	#print "srv.parseHeader hat folgende Daten:\n"
	#print data

	header_and_body = data.split("\r\n\r\n") # header und body trennen

	http_header = header_and_body[0]
	#http_body = header_and_body[1] # body brauchen wir hier nicht

	print http_header

	header_lines = http_header.split("\r\n") # Header in einzelne Zeilen aufteilen

	h_first_line = header_lines[0] # erste Zeile, die hier fuer uns extrem wichtig ist

	space_parts = h_first_line.split(" ")


	# Jede HTTP-Anfrage sieht so aehnlich aus:
	#
	# GET /resource_name.html HTTP/1.0
	# ^  ^ ^                 ^ ^
	# |  | |                 | |
	# |  | |                 | + Protokoll/Version
	# |  | |                 + Leerzeichen
	# |  | + Resource
	# |  + Leerzeichen
	# + Method
	#
	# Ergibt also exakt 3 Parts, die durch ein Leerzeichen getrennt sind
	if len(space_parts) != 3 :
		print "kein gueltige http anfrage"
		return

	http_method = space_parts[0]
	http_request_file = space_parts[1]

	http_protocol = space_parts[2].split("/")[0] # Protokoll und P.-Version sind immer durch ein / getrennt
	http_version = space_parts[2].split("/")[1]

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

		for key_value_pair in params: # params = ['a=val', 'b=other']

			# z.B.: key_value_pair = 'a=val'
			if key_value_pair.find("=") > 0:  # Parameter koennen auch OHNE Wert angegeben werden...!
				key = key_value_pair.split("=")[0]
				value = key_value_pair.split("=")[1]
			else:
				key = key_value_pair
				value = None

			url_params[urllib.unquote(key)] = urllib.unquote(value)

	# Zur Kontrolle / Uebersicht einfach mal alles ausgeben
	print "URL-Parameter: %s"%url_params
	print "HTTP-Protcol: %s"%http_protocol
	print "HTTP-Version: %s"%http_version
	print "HTTP-Method: %s"%http_method
	print "HTTP-Req.-File: %s"%http_request_file

	request = {"protocol":http_protocol, "version":http_version, "method":http_method, "resource":http_request_file, "params":url_params}
	return request

# ausgelagerte 200 Status Funktion
def status200(conn, request):
	conn.send("HTTP/1.0 200 OK\r\n")
	conn.send("Content-Type: text/html; charset=utf8\r\n")
	conn.send("\r\n")

# ausgelagerte 404 Status Funktion
def status404(conn, request):
	conn.send("HTTP/1.0 404 Not Found\r\n")
	conn.send("Content-Type: text/html; charset=utf8\r\n")
	conn.send("\r\n")
	conn.send("<h1>Not Found</h1><p>The requested URL %s was not found on this server</p>"%request['resource'])

# ausgelagerte 500 Status Funktion
def status500(conn, request):
	conn.send("HTTP/1.0 500 Server Error\r\n")
	conn.send("Content-Type: text/html; charset=utf8\r\n")
	conn.send("\r\n")
	conn.send("<h1>Server Error</h1><p>The requested URL %s created a fatal error 500 on this server</p>"%request['resource'])

def status():
	return "ok"
