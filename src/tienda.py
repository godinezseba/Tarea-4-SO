import threading


class Clientes(threading.Thread):
    def __init__(self, Scola, Satendido, Sclientes):
        threading.Thread.__init__(self)
        self.Scola = Scola
        self.Satendido = Satendido
        self.Sclientes = Sclientes
        self.clientes = 0

    def run(self):

        self.Scola.acquire()
        if(not(self.clientes < 30)):
            self.Scola.release()
            print "cliente " + self.name + " se fue"
            return
        self.clientes += 1
        self.Scola.release()
        # aviso llegue
        self.Sclientes.release()
        # espero pasar
        self.Satendido.acquire()
        print "cliente " + self.name + " se corto el pelito"
        # se vira


class Barbero(threading.Thread):
    def __init__(self, Scola, Satendido, Sclientes):
        threading.Thread.__init__(self)
        self.Scola = Scola
        self.Satendido = Satendido
        self.Sclientes = Sclientes
        self.cant = 0

    def run(self):
        while self.cant < 30:  # REVISAR condicion de termino
            self.Sclientes.acquire()
            self.Satendido.release()
            self.cant += 1
            print "estoy cortando el pelito, clientes atendidos: " + \
                str(self.cant)
