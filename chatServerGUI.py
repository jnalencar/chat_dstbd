import tkinter as tk
import subprocess

class ChatAppGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chat DSTBD")
        
        self.server_process = None
        self.binder_process = None

        self.start_button = tk.Button(master, text="Iniciar Servidor", command=self.start_server)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Parar Servidor", command=self.stop_server)
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(master, text="Servidor não está rodando")
        self.status_label.pack(pady=10)

    def start_server(self):
        try:
            if self.binder_process is None:
                self.binder_process = subprocess.Popen(["python", "binder.py"])
            if self.server_process is None:
                self.server_process = subprocess.Popen(["python", "server.py"])
                self.status_label.config(text="Servidor está rodando")
            else:
                self.status_label.config(text="Servidor já está rodando")
        except Exception as e:
            self.status_label.config(text=f"Erro ao iniciar o servidor: {e}")

    def stop_server(self):
        try:
            if self.server_process:
                self.server_process.terminate()
                self.server_process = None
            if self.binder_process:
                self.binder_process.terminate()
                self.binder_process = None
            self.status_label.config(text="Servidor parado")
        except Exception as e:
            self.status_label.config(text=f"Erro ao parar o servidor: {e}")

root = tk.Tk()
app = ChatAppGUI(root)
root.mainloop()