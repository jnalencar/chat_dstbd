from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import threading
import time

class ChatServer:
    def __init__(self):
        self.users = {}
        self.rooms = {}
        self.lock = threading.Lock()

    def register_user(self, username):
        with self.lock:
            if username in self.users:
                return False
            self.users[username] = []
            return True

    def create_room(self, room_name):
        with self.lock:
            if room_name in self.rooms:
                return False
            self.rooms[room_name] = {'users': [], 'messages': []}
            return True

    def join_room(self, username, room_name):
        with self.lock:
            if room_name not in self.rooms or username not in self.users:
                return None
            if username not in self.rooms[room_name]['users']:
                self.rooms[room_name]['users'].append(username)
                self.users[username].append(room_name)
                message = {
                    'type': 'broadcast',
                    'origin': 'Sistema',
                    'destination': 'Todos',
                    'content': f'{username} entrou na sala.',
                    'timestamp': time.time()
                }
                self.rooms[room_name]['messages'].append(message)
            users = self.rooms[room_name]['users']
            messages = self.rooms[room_name]['messages'][-50:]
            return users, messages

    def send_message(self, username, room_name, message, recipient=None):
        with self.lock:
            if room_name not in self.rooms or username not in self.users:
                return False
            msg = {
                'type': 'unicast' if recipient else 'broadcast',
                'origin': username,
                'destination': recipient if recipient else 'Todos',
                'content': message,
                'timestamp': time.time()
            }
            self.rooms[room_name]['messages'].append(msg)
            return True

    def receive_messages(self, username, room_name, last_timestamp):
        with self.lock:
            if room_name not in self.rooms or username not in self.users:
                return []
            messages = []
            for msg in self.rooms[room_name]['messages']:
                if msg['timestamp'] > last_timestamp:
                    if msg['type'] == 'broadcast' or msg['destination'] == username:
                        messages.append(msg)
            return messages

    def list_rooms(self):
        with self.lock:
            return list(self.rooms.keys())

    def list_users(self, room_name):
        with self.lock:
            if room_name in self.rooms:
                return self.rooms[room_name]['users']
            return []

    def remove_user(self, username, room_name):
        with self.lock:
            if room_name in self.rooms and username in self.rooms[room_name]['users']:
                self.rooms[room_name]['users'].remove(username)
                if not self.rooms[room_name]['users']:
                    threading.Timer(300, self.remove_room, args=[room_name]).start()
                message = {
                    'type': 'broadcast',
                    'origin': 'Sistema',
                    'destination': 'Todos',
                    'content': f'{username} saiu da sala.',
                    'timestamp': time.time()
                }
                self.rooms[room_name]['messages'].append(message)

    def remove_room(self, room_name):
        with self.lock:
            if room_name in self.rooms and not self.rooms[room_name]['users']:
                del self.rooms[room_name]

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 0), allow_none=True)
    port = server.server_address[1]
    chat_server = ChatServer()
    server.register_instance(chat_server)
    binder = xmlrpc.client.ServerProxy("http://localhost:5000/")
    procedures = ['register_user', 'create_room', 'join_room', 'send_message', 'receive_messages', 'list_rooms', 'list_users', 'remove_user']
    for proc in procedures:
        binder.register_procedure(proc, 'localhost', port)
    print(f"Servidor executando na porta {port}...")
    server.serve_forever()