import asyncio


global_dict = {}


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        data = data.decode('utf-8')
        self.transport.write(self._process(data.strip('\r\n')).encode('utf-8'))

    def _process(self, command):
        split_command = command.split(' ')
        if split_command[0] == 'get' and len(split_command) == 2:
            return self._get(split_command[1])
        if split_command[0] == 'put' and len(split_command) == 4:
            try:
                return self._put(split_command[1], float(split_command[2]), int(split_command[3]))
            except ValueError:
                return 'error\nwrong command\n\n'
        else:
            return 'error\nwrong command\n\n'

    def _get(self, key):
        answer = 'ok\n'
        data = global_dict
        # for key, ts in global_dict.items():
        #     global_dict[key] = sorted(ts.items())
        # if len(global_dict[key]) != 0:
        #     global_dict[key].sort(key=lambda tup: tup[0])
        # for key, ts in global_dict.items():
        #     global_dict[key] = sorted(ts.it)
        # if key == '*':
        #     for key, values in global_dict.items():
        #         for value in values:
        #             answer = answer + key + ' ' + value[1] + ' ' + value[0] + '\n'
        # else:
        if key != '*':
            data = {key: data.get(key, {})}
            # if key in global_dict:
        res = {}
        # if key == '*':
        #     for key, values in data.items():
        #         for ts, value in values:
        #             print(ts)
        #             print(value)
        #             # answer = answer + key + ' ' + ts + ' ' + value + '\n'
        # else:
        for key, ts in data.items():
            res[key] = sorted(ts.items())
        # print(res.items())
        for key, values in res.items():
            for timestamp, value in values:
            # print(value)
                answer = answer + key + ' ' + str(value) + ' ' + str(timestamp) + '\n'
                # print(answer)
        return answer + '\n'

    def _put(self, key, value, timestamp):
        if key not in global_dict:
            global_dict[key] = {}
        global_dict[key][timestamp] = value
        # global_dict[key].sort(key=lambda tup: tup[0])
        return 'ok\n\n'


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

#
# run_server('127.0.0.1', 9999)
