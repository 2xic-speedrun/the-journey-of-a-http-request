import socket
from dns import get_ip

class Http:
    def get(self, ip, host, path):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((ip, 80))
        encoded = self.construct_get(host)    
        print(encoded)
 
        clientSocket.send(
            encoded
        )
        response = bytes([])
        SIZE = 128
        while True:
            read = clientSocket.recv(SIZE)
            response += read
            if len(read) == 0 or len(read) < SIZE:
                break
        return response

    def construct_get(self, host):
        lines = [
            "GET / HTTP/1.1",
            "Host: www." + host,
            "Accept-Language: en",
            "",
            ""
        ]
        return "\r\n".join(lines).encode()

if __name__ == "__main__":
    host  = "google.com"
    ip = get_ip(host)
    response = Http().get(ip, host, "/") 
    print(response)

