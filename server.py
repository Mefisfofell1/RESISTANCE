import socket
from threading import Thread
from time import sleep
import datetime


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
            i.settimeout(20.2)
        # Socket load info
        self.socket_busy = [False for i in range(self.max_clients)]
        # Blacklist
        self.blacklist = ["127.0.0.1"] + Log.read_n_return_list("blacklist.txt")
        # Server socket
        self.server_socket = socket.socket()
        # Server timeout
        self.server_socket.settimeout(20.2)
        # Server bind
        self.server_socket.bind(("26.155.142.20", self.port))
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
            thread = Thread(target=self.__connect, args=(address, 1))
            thread.start()
            thread.join(0)
            self.client_sockets[find], address = self.server_socket.accept()
            self.client_sockets[find].settimeout(0.2)
        except OSError:
            self.log.save_data("Failed to create session with {}".format(address))
            self.__del_user(address)
            return

    # Connect to user
    def __connect(self, address: str, *args):
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

    # Closes connection
    def close_connection(self, address: str):
        find = self.__get_find_address(address)
        self.__reload_socket(find)
        self.__del_user(address)

    # Stops server
    def kill_server(self):
        self.run = False
        sleep(1)
        self.server_socket.close()
        self.log.kill_log()
        for i in self.client_sockets:
            i.close()
        for i in self.clients_logs:
            try:
                i.kill_log()
            except TypeError:
                pass

    # Send messages
    def send(self, address: str, message: bytes):
        find = self.__get_find_address(address)
        print(find)
        try:
            self.client_sockets[find].send(message)
            self.clients_logs[find].save_data("to {}: {}".format(address, message))
            self.log.save_data("Send message to {}".format(address))
        except OSError:
            self.log.save_data("Send to {} Failed".format(address))

    # Adds user
    def __add_user(self, address: str):
        find = self.__get_free_socket()
        self.clients_logs[find] = Log("{}.log".format(address))
        self.max_clients_ip[find] = address
        self.incoming_requests[address] = []
        self.log.save_data("Added user {}".format(address))

    # Adds incoming request
    def __add_request(self, address: str, message: bytes):
        self.incoming_requests[address].append(message.decode("utf-8"))
        self.clients_logs[self.__get_find_address(address)].save_data("from {}: {}".format(address, str(message)))
        self.log.save_data("Get incoming message from {}".format(address))

    # Returns an index of the 1st available socket
    def __get_free_socket(self):
        for i in range(len(self.socket_busy)):
            if not self.socket_busy[i]:
                return i
        return None

    # Returns an index given to user
    def __get_find_address(self, address: str):
        for i in range(len(self.max_clients_ip)):
            if self.max_clients_ip[i] == address:
                return i
        else:
            return None

    # Checks requests
    def check_request(self, address: str):
        return bool(self.incoming_requests.get(address))

    # Returns True if you have already connected to address
    def check_address(self, address: str):
        return True if address in self.max_clients_ip else False

    # Deletes user
    def __del_user(self, address: str):
        find = self.__get_find_address(address)
        self.clients_logs[find].kill_log()
        self.clients_logs[find] = Log
        self.max_clients_ip[find] = ""
        self.incoming_requests.pop(address)
        self.log.save_data("Deleted user {}".format(address))

    # Returns an amount of connected users
    def __len__(self):
        length = 0
        for i in self.max_clients_ip:
            if i != "":
                length += 1
        return length

    # Returns True if there is at least one connection
    def __bool__(self):
        for i in self.max_clients_ip:
            if i != "":
                return True
        return False


class Log:
    def __init__(self, name: str):
        self.name = name
        try:
            self.file = open(name, "a")
        except FileNotFoundError:
            self.file = open(name, "w")
        self.save_data("Log started at " + str(datetime.datetime.now()))
        self.file.close()

    # Saves information to file
    def save_data(self, data: str):
        self.file = open(self.name, "a")
        self.file.write("{}\n".format(data))
        self.file.close()

    # Returns data from file as list
    @staticmethod
    def read_n_return_list(name: str):
        try:
            file = open(name, "r")
        except FileNotFoundError:
            return []
        data = file.read()
        return data.split("\n")

    # Shuts log
    def kill_log(self):
        self.file = open(self.name, "a")
        self.save_data("Log stopped at {}\n".format(datetime.datetime.now()))
        self.file.close()
