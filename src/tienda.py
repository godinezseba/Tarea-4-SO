import threading

class Clientes(threading.Thread):
    def __init__(self, Scola, Satendido, Sclientes, clientes):
        threading.Thread.__init__(self)
        self.Scola = Scola
        self.Satendido = Satendido
        self.Sclientes = Sclientes
        self.clientes = clientes
    def run(self):
        
        self.Scola.acquire()
        if(self.clientes >= 30+1):
            self.Scola.release()
            exit()
        self.clientes+=1
        self.Scola.release()
        #aviso llegue
        self.Sclientes.release()
        #espero pasar
        self.Satendido.acquire()
        print("clientes " + self.name + " se corto el pelito")
        # se vira
        self.Scola.acquire()
        self.clientes=-1
        self.Scola.release()
    


class Barbero(threading.Thread):
    def __init__(self, Scola, Satendido, Sclientes):
        threading.Thread.__init__(self)
        self.Scola = Scola
        self.Satendido = Satendido
        self.Sclientes = Sclientes
    def run(self):
        while True:
            self.Sclientes.acquire()
            self.Satendido.release()
            print("estoy cortando el pelito")