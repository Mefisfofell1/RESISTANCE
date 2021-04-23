import socket
from threading import Thread
from time import sleep


class P2P:
    def __init__(self, port: int, max_clients):
        # Server work indicator
        self.run = True
        # Server port
        self.port = port
        # Max amount of connections
        self.max_clients = max_clients
        # Connected users
        self.max_clients_ip = ["" for i in range(self.max_clients)]
        # Dictionary with incoming messages
        self.incoming_requests = {}
        # Client logs
        self.clients_logs = [Log for i in range(self.max_clients)]
        # Client sockets
        self.client_sockets = [socket.socket() for i in range(self.max_clients)]
        # Client timeouts
        for i in self.client_sockets:
            i.settimeout(0.2)
        # Socket load info
        self.socket_busy = [False for i in range(self.max_clients)]
        # Blacklist
        self.blacklist = ["127.0.0.1"] + Log.read_n_return_list("blacklist.txt")
        # Server socket
        self.server_socket = socket.socket()
        # Server timeout
        self.server_socket.settimeout(0.2)
        # Server bind
        self.server_socket.bind(("localhost", port))
        self.server_socket.listen(self.max_clients)
        self.log = Log("sever.log")
        self.log.save_data("Server initialized")

    # Creates session with user
    def create_session(self, address: str):
        self.log.save_data("Creating session with {}".format(address))
        find = self.__get_free_socket()
        if address in self.blacklist:
            self.log.save_data("{} in blacklist".format(address))
            return
        if find is None:
            self.log.save_data("All sockets are busy, can't connect to {}".format(address))
            return
        try:
            self.__add_user(address)
            thread = Thread(target=self.__connect, args=(address, 1))  # TODO
            thread.start()
            thread.join(0)
            connection, address = self.server_socket.accept()
            connection.settimeout(0.2)
        except OSError:
            self.log.save_data("Failed to create session with {}".format(address))
            self.__del_user(address)  # TODO
            return

    # Connect to user
    def __connect(self, address: str):
        find = self.__get_find_address(address)
        try:
            self.client_sockets[find].connect((address, self.port))
            self.socket_busy[find] = True
            return True
        except OSError:
            return False

    # Reloads socket
    def __reload_socket(self, find: int):
        self.client_sockets[find].close()
        self.client_sockets[find] = socket.socket()
        self.socket_busy[find] = False

    # Returns index of 1st available socket
    def __get_free_socket(self):
        for i in range(len(self.socket_busy)):
            if not self.socket_busy[i]:
                return i
        return None
