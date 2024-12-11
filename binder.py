# binder.py

from xmlrpc.server import SimpleXMLRPCServer

class Binder:
    def __init__(self):
        self.procedures = {}

    def register_procedure(self, name, address, port):
        self.procedures[name] = (address, port)
        return True

    def lookup_procedure(self, name):
        return self.procedures.get(name, None)

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 5000))
    binder = Binder()
    server.register_function(binder.register_procedure, "register_procedure")
    server.register_function(binder.lookup_procedure, "lookup_procedure")
    print("Binder executando na porta 5000...")
    server.serve_forever()