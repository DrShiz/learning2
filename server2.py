import asyncio


class GlobalDict:
    def __init__(self):
        self._data = {}

    def put(self, key, value, timestamp):
        if key not in self._data:
            self._data[key] = {}
        self._data[key][timestamp] = value

    def get(self, key):
        data = self._data
        if key != "*":
            data = {key: data.get(key, {})}
        result = {}
        for key, timestamp_data in data.items():
            result[key] = sorted(timestamp_data.items())
        return result


class GetError(Exception):
    pass


class Parser:
    def encode(self, responses):
        rows = []
        for response in responses:
            if not response:
                continue
            for key, values in response.items():
                for timestamp, value in values:
                    rows.append(f"{key} {value} {timestamp}")
        result = "ok\n"
        if rows:
            result += "\n".join(rows) + "\n"
        return result + "\n"

    def decode(self, data):
        parts = data.split("\n")
        commands = []
        for part in parts:
            if not part:
                continue
            try:
                method, params = part.strip().split(" ", 1)
                if method == "put":
                    key, value, timestamp = params.split()
                    commands.append((method, key, float(value), int(timestamp)))
                elif method == "get":
                    key = params
                    commands.append((method, key))
                else:
                    raise GetError()
            except GetError:
                raise GetError()

        return commands


class Exe:
    def __init__(self, storage):
        self.storage = storage

    def run(self, method, *params):
        if method == "put":
            return self.storage.put(*params)
        elif method == "get":
            return self.storage.get(*params)


class ClientServerProtocol(asyncio.Protocol):
    dict = GlobalDict()

    def __init__(self):
        super().__init__()
        self.parser = Parser()
        self.executor = Exe(self.storage)
        self._buffer = b''

    def process(self, data):
        commands = self.parser.decode(data)
        responses = []
        for command in commands:
            resp = self.executor.run(*command)
            responses.append(resp)
        return self.parser.encode(responses)

    def connection_made(self, transport):
        self.transport = transport


def data_received(self, data):
    self._buffer += data
    try:
        decoded_data = self._buffer.decode()
    except GetError():
        return
    if not decoded_data.endswith('\n'):
        return
    self._buffer = b''
    try:
        resp = self.proccess(decoded_data)
    except GetError as err:
        self.transport.write(f"error\n{err}\n\n".encode())
        return
    self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    run_server('127.0.0.1', 9999)