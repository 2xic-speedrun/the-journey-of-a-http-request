import socket
import sys
from functools import reduce
from dns_response import DnsResponse

def create_n_bytes(x: bytes, n: int):
    if len(x) < n:
        x = bytes([0, ]) * (n - len(x)) + x
    return x

def encode_domain(domain):
    return reduce(lambda x,y: x+ y, [
        bytes([len(i)]) + bytes([ord(v) for v in i])
        for i in domain.split(".")
    ])

def create_question_section():
    qname = "www.google.com"
    encoded_name = encode_domain(qname)
    
    # bytes([len(qname)]) + qname.encode() + bytes([0])
    q_type = bytes([0, 1])  # A-Record bytes([255])
    q_class = bytes([0, 1]) # in-class bytes([255])
    return encoded_name + q_type + q_class

def create_byte_string(list_of_bits: list[str], length):
    output = int(''.join(list_of_bits), 2)
    print(output)
    response = []
    while 0 < output:
        res = output & 0xFF
        response.append(res)
        output >>= 8 
    response = list(reversed(response))
    if len(response) < length:
        response += [0, ] * (length - len(response))
    return response

assert encode_domain("image.google.com") == bytes([
    5,
]) + "image".encode() + bytes([
    6
]) + "google".encode() + bytes([
    3
]) + "com".encode()

control = bytes(create_byte_string([
        # Control / QR   (request = 0, response = 1) 
        '0'
        # Control / Opcode
        # 0000 = standard query
        '0000',
        # Control / Authoritative (1 = authoritative and 0 = cache)
        '0',
        # Truncated (1 if larger than 512 bits)
        '0',
        # RD (recursion desired)
        '1',
        # RA (recursion available)
        '0',
        # reserved for extensions 
        '0',
        # reserved for DNSSEC 
        '0',
        # reserved for DNSSEC 
        '0',  
        # reserved for error codes 
        '0000',
    ], 2))
assert len(control) == 2, len(control)
bits = "{0:b}".format(control[0], control[1])
assert control == b"\x01\x00"

request = [
    # Identification 
    create_n_bytes(bytes([0x24, 0x1a]), 2),
    control,
    # question count
    create_n_bytes(bytes([1]), 2),
    # answered count
    create_n_bytes(bytes([0]), 2),
    # name server recourses count
    create_n_bytes(bytes([0]), 2),
    # additional records count
    create_n_bytes(bytes([0]), 2),
]
request_with_payload = request + [create_question_section()]
header_bytes = reduce(lambda x, y: x+ y, request)
request_bytes = reduce(lambda x, y: x+ y, request_with_payload)

assert len(header_bytes) == 2 * 6,  len(header_bytes)
bytes = bytes([0x01,0x00,0x00,0x01])
assert request_bytes[2:len(bytes) + 2] == bytes, request_bytes[2:len(bytes) + 2]

if "try" in sys.argv:
    print("sending ", request_bytes)
    assert len(request_bytes) < 512, "use tcp"

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)# socket.SOCK_STREAM)
    clientSocket.connect(("8.8.8.8", 53))
    clientSocket.send(request_bytes)
    response = clientSocket.recv(2048)

    print("received " , response)

    request = DnsResponse(request_bytes, comment="Request sent")
    response = DnsResponse(response, comment="Response gotten")
    print(response)
    print(request)
    while True:
        response = clientSocket.recv(2048)
        print(response)
else:
    print("would send ", request_bytes)
