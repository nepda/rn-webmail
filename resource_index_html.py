import sys, traceback


REQUEST = ""
MAIL_SERVER = ""
MAIL_PORT = ""
MAIL_USER = ""
MAIL_PASS = ""

CONN = None

msrv = None

def main(conn, request):
	conn.send("HTTP/1.0 200 OK\r\n")
	conn.send("Content-Type: text/html; charset=utf8\r\n")
	conn.send("\r\n")
	conn.send("<h1>Index Ressource</h1>")
	
	
	MAIL_SERVER = "dem.informatik.tu-chemnitz.de"
	MAIL_PORT   = 110
	MAIL_USER   = "rot"
	MAIL_PASS   = "rot"
	
	CONN = conn
	REQUEST = request
	
	
	
	
	if len(REQUEST['params']) > 0:
		if 'mail_server' in REQUEST['params'].keys():
			MAIL_SERVER = REQUEST['params']['mail_server']
			
		if 'mail_port' in REQUEST['params'].keys():
			MAIL_PORT = REQUEST['params']['mail_port']
			
		if 'mail_user' in REQUEST['params'].keys():
			MAIL_USER = REQUEST['params']['mail_user']
			
		if 'mail_pass' in REQUEST['params'].keys():
			MAIL_PASS = REQUEST['params']['mail_pass']
	
	html = "<p>Verbindung wird augebaut mit:<br/>"
	html += "Server: %s<br/>"%MAIL_SERVER
	html += "Port: %s<br/>"%MAIL_PORT
	html += "User: %s<br/>"%MAIL_USER
	html += "Pass: *****<br/>"
	
	html += "</p>"
	
	CONN.send(html)
	
	
	
	try:
		import Mail
		reload(Mail)
		try:
			msrv = Mail.Mail(conn, request)
			if msrv.verbinden(MAIL_SERVER, MAIL_PORT):
				
				if not msrv.anmelden(MAIL_USER, MAIL_PASS):
					CONN.send("Konnte nicht einloggen")
					return 0
				
				if len(REQUEST['params']):
					if 'getmail' in REQUEST['params'].keys():
						get_mail(REQUEST['params']['getmail'])
					else:
						list_mails()
				else:
					list_mails()
				
			else:
				CONN.send("<br/>Verbindung konnte nicht aufgebaut werden")
			
		except:
			print "Unexpected error:", sys.exc_info()
			raise
			CONN.send("Mail modul spinnt")
	except:
		print traceback.print_tb(sys.exc_info()[2])
		CONN.send("Modul Mail not found")
		print "Modul Mail not found"
		return 0
	
def list_mails():
	print MAIL_SERVER, MAIL_PORT, MAIL_PASS, MAIL_USER, CONN, msrv
	default_url = "index.html?mail_server="+MAIL_SERVER+"&mail_port="+MAIL_PORT+"&mail_user="+MAIL_USER+"&mail_pass="+MAIL_PASS
	
	print msrv
	
	l = msrv.list_mails()
	
	html = "<table border='1'>"
	for item in l:
		html = html + "<tr>"
		html = html + "<td><a href=\""+default_url+"&getmail="+item[0]+"\">"+item[0]+"</a></td><td><a href=\""+default_url+"&getmail="+item[0]+"\">"+item[1]+"</a></td>"
		html = html + "</tr>"
	
	html = html + "</table>"
	CONN.send(html)

def get_mail(mail_nr):
	CONN.send("try to fetch mail with number: "+mail_nr)
