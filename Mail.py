import sys, socket

class Mail:
	conn = 0
	req = 0
	msock = 0
	c_okay = 0
	def __init__(self, conn, req):
		self.conn = conn
		self.req = req
		
		self.msock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
	def recvline (self, conn) :
		data = ''
		while 1:
			d = conn.recv(1)
			if d == '\n' :
				break
			if d != '\r' :
				data = data + d
		return data
		
	def verbinden(self, hostname, port):
		
		try:
			self.msock.connect((hostname, port))
			
			answer = self.recvline(self.msock)
			
			#self.conn.send("Antwort: <pre>" + answer + "</pre>")
			
			if answer[:1] == "+" :
				#self.conn.send("<br/>Verbindung erfolgreich hergestellt")
				self.c_okay = 1
				return 1
			else:
				#self.conn.send("<br/>Verbindung abgelehnt")
				self.c_okay = 0
				return 0
		except:
			#self.conn.send("<br/>Verbindung wurde zurueckgewiesen:<br/>")
			print sys.exc_info()
		
		self.c_okay = 0
		return 0
	
	def anmelden(self, benutzer, passwort):
		if not self.c_okay :
			self.conn.send("<br/>Anmelden nicht moeglich, Verbindung nicht okay")
			return 0
		
		cmd = "USER "+benutzer + "\r\n"
		self.msock.send(cmd)
		
		answer = self.recvline(self.msock)
		if not answer[:1] == "+":
			print "set user: login error"
			return 0
		
		
		cmd = "PASS "+passwort + "\r\n"
		self.msock.send(cmd)
		
		answer = self.recvline(self.msock)
		if not answer[:1] == "+":
			print "set user: login error"
			return 0
		return 1
		
		
	def list_mails(self):
		if not self.c_okay :
			self.conn.send("<br/>Anmelden nicht moeglich, Verbindung nicht okay")
			return 0
		
		self.msock.send("LIST\r\n")
		
		
		status= self.recvline(self.msock)
		if not status[:1] == "+":
			# liste konnte nicht erhalten werden
			return 0
		
		mail_list = list();
		ok = 1
		while ok:
			item = self.recvline(self.msock)
			if item == ".":
				ok = 0
				break
			mail_list.append( item.split(" ") )
			#print item
		
		#print "------------------------ : LIST"
		return mail_list
	
	def __exit__(self, exc_type, exc_value, traceback):
		if (self.msock):
			self.msock.close()
