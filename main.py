
import time, socket, sys
import srv

print "- - - - Server nepdaPy started - - - - - - - - - - - - - - - - "

if len(sys.argv) != 2:
	print "Benutzung: python %s <port>"%sys.argv[0]
	sys.exit(1)

try:
	port = int(sys.argv[1])
except:
	print "%s ist keine gueltige Portnummer"%sys.argv[1]
	sys.exit()

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("", port))
	s.listen(1)
	
	while srv.status() != "quit" :
		conn, addr = s.accept()
		print "Verbindung von Host %s, port %d"%(addr[0], addr[1])
		data = conn.recv(2048)
		if not data :
			break
		#print "daten empfangen"
		reload(srv)
		srv.main(conn, data)
		conn.close()
	s.close()
except:
	print "Unexpected error:", sys.exc_info()
	print "Server error"
	sys.exit(1)

print "- - - - Server nepdaPy started - - - - - - - - - - - - - - - - "
