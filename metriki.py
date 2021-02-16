import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, address, port, timeout=None):
        self.address = address
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((self.address, self.port), self.timeout)

    def _read(self):
        recv_data = b""
        while not recv_data.endswith(b"\n\n"):
            try:
                recv_data += self.sock.recv(1024)
            except socket.error as err:
                raise ClientError()
        decoded_recv_data = recv_data.decode('utf-8')
        status, payload = decoded_recv_data.split("\n", 1)
        payload = payload.strip()
        # print(payload)
        # print(payload.split("\n"))
        # print(len(payload.split("\n")))
        # if len(payload.split("\n")) != 3:
        #     raise ClientError()
        if status != 'ok':
            raise ClientError()
        return payload

    def get(self, key):
        senddata = 'get' + ' ' + str(key) + '\n'
        # print(senddata)
        # try:
        self.sock.sendall(senddata.encode('utf-8'))
        # except socket.error as err:
        #     raise ClientError()
        payload = self._read()
        dict = {}
        if payload == "":
            return dict
        for row in payload.split("\n"):
            if len(row.split()) != 3:
                raise ClientError()
            key, value, timestamp = row.split()
            if key not in dict:
                dict[key] = []
            dict[key].append((int(timestamp), float(value)))
            dict[key].sort(key=lambda tup: tup[0])
        return dict
        # print(data)

    def put(self, key, value, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())
        senddata = 'put' + ' ' + str(key) + ' ' + str(value) + ' ' + str(timestamp) + '\n'
        try:
            self.sock.sendall(senddata.encode("utf8"))
        except socket.error as err:
            raise ClientError()
        self._read()


client = Client("127.0.0.1", 9999, timeout=15)
client.put('palm.cpu', '10.5', '1501864247')
print(client.get('palm.cpu'))
# data1 = 'ok\npalm.cpu 10.5 1501864247\npalm.cpu 10.5 1501864248\neardrum.cpu 15.3 1501864259\n\n'
# data = data1.split('\n')
# print(data)
# print('')
# data.pop(0)
# data.pop(-1)
# data.pop(-1)
# print(data)
# print('')
# dict = {}
# list = []
# for i in data:
#     print(i)
#     list.append((int(i.split(' ')[2]), float(i.split(' ')[1])))
#     print(list)
#     dict[i.split(' ')[0]] = list
#     print(dict)
#     print('')
# dict = {'key': [(1501865247, 13.045), (1501864247, 10.5), (1501864243, 11.0), (1501864248, 22.5)]}
# list_d = list(dict.items())
# print(list_d)
# list_d.sort(key=lambda i: i[1][0])
# print(list_d)
# data = 'palm.cpu 10.5 1501864247\npalm.cpu 10.5 1501864248\neardrum.cpu 15.3 1501864259\npalm.cpu 10.5 1501864250\npalm.cpu 10.5 1501864230\neardrum.cpu 15.3 1501864250\npalm.cpu 10.5 1501864233\npalm.cpu 10.5 1501864240\neardrum.cpu 15.3 1501864251'
# for row in data.split("\n"):
#     key, value, timestamp = row.split()
# print(sorted(data, key=data.split("\n").split()))
