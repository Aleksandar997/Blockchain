import socket

class Sockets(list):
    def append_socket(self, host, port, maximum_connections):
        try:
            self.append({
                'socket': socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                'port': port
            })
            self[-1]['socket'].setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
            self[-1]['socket'].bind((host, port)) 
            self[-1]['socket'].listen(maximum_connections) 
        except socket.error:
            if self[-1]:
                self[-1].close()
                self = self[:-1]

    def get_sockets(self):
        return map(lambda s: s['socket'], self)