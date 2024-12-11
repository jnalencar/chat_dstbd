# client.py

import xmlrpc.client
import threading
import time

class ChatClient:
    def __init__(self):
        self.binder = xmlrpc.client.ServerProxy("http://localhost:5000/")
        self.username = None
        self.room_name = None
        self.last_timestamp = time.time()

    def get_server(self, procedure_name):
        info = self.binder.lookup_procedure(procedure_name)
        if info:
            address, port = info
            return xmlrpc.client.ServerProxy(f'http://{address}:{port}/', allow_none=True)
        return None

    def register_user(self):
        while True:
            username = input("Digite um username único: ")
            server = self.get_server('register_user')
            if server.register_user(username):
                self.username = username
                print("Registrado com sucesso.")
                break
            else:
                print("Username já em uso, tente novamente.")

    def create_room(self):
        room_name = input("Nome da sala: ")
        server = self.get_server('create_room')
        if server.create_room(room_name):
            print("Sala criada com sucesso.")
        else:
            print("Nome da sala já existe.")

    def join_room(self):
        room_name = input("Nome da sala: ")
        server = self.get_server('join_room')
        result = server.join_room(self.username, room_name)
        if result:
            users, messages = result
            self.room_name = room_name
            print("Entrou na sala com sucesso.")
            print("Usuários na sala:", users)
            print("Últimas mensagens:")
            for msg in messages:
                print(f"{msg['origin']}: {msg['content']}")
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.chat()
        else:
            print("Sala não encontrada.")

    def send_message(self):
        message = input("Mensagem: ")
        recipient = input("Destinatário (vazio para todos): ")
        server = self.get_server('send_message')
        server.send_message(self.username, self.room_name, message, recipient if recipient else None)

    def receive_messages(self):
        server = self.get_server('receive_messages')
        while True:
            messages = server.receive_messages(self.username, self.room_name, self.last_timestamp)
            for msg in messages:
                print(f"{msg['origin']}: {msg['content']}")
                self.last_timestamp = msg['timestamp']
            time.sleep(2)

    def list_rooms(self):
        server = self.get_server('list_rooms')
        rooms = server.list_rooms()
        print("Salas disponíveis:", rooms)

    def list_users(self):
        server = self.get_server('list_users')
        users = server.list_users(self.room_name)
        print("Usuários na sala:", users)

    def remove_user(self):
        server = self.get_server('remove_user')
        server.remove_user(self.username, self.room_name)
        self.room_name = None

    def chat(self):
        while True:
            cmd = input("[Enviar mensagem (m), Listar usuários (l), Sair da sala (s)]: ")
            if cmd == 'm':
                self.send_message()
            elif cmd == 'l':
                self.list_users()
            elif cmd == 's':
                self.remove_user()
                break

    def start(self):
        self.register_user()
        while True:
            cmd = input("[Criar sala (c), Entrar em sala (e), Listar salas (l), Sair (s)]: ")
            if cmd == 'c':
                self.create_room()
            elif cmd == 'e':
                self.join_room()
            elif cmd == 'l':
                self.list_rooms()
            elif cmd == 's':
                break

if __name__ == "__main__":
    client = ChatClient()
    client.start()