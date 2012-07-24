import sys, cfg

def main(conn, request):
	conn.send("HTTP/1.0 200 OK\r\n")
	conn.send("Content-Type: text/html; charset=utf8\r\n")
	conn.send("\r\n")
	conn.send("<h1>Index Ressource</h1>")
	
	try:
		import Mail
		reload(Mail)
		try:
			m = Mail.Mail(conn, request)
			if m.verbinden(cfg.mail_server, cfg.mail_port):
				
				
				if not m.anmelden(cfg.mail_user, cfg.mail_pass):
					conn.send("Login nicht erfolgreich")
				
				l = m.list_mails()
				
				html = "<table border='1'>"
				for item in l:
					html = html + "<tr>"
					html = html + "<td>"+item[0]+"</td><td>"+item[1]+"</td>"
					html = html + "</tr>"
				
				html = html + "</table>"
				conn.send(html)
			else:
				conn.send("<br/>Verbindung konnte nicht aufgebaut werden")
			
		except:
			print "Unexpected error:", sys.exc_info()
			raise
			conn.send("Mail modul spinnt")
	except:
		print "Unexpected error:", sys.exc_info()
		conn.send("Modul Mail not found")
		print "Modul Mail not found"
		return 0
	
	


