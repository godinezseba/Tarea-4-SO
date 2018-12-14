import threading
from time import sleep


class Tienda():
    def __init__(self, cantidad):
        self.capacidad = 30  # total gente que puede estar dentro
        self.gente = 0  # gente actual dentro de la tienda
        self.total = cantidad  # total de gente a atender
        self.totalgente = 0  # cantidad de gente atendida
        # semaforo para controlar la gente que entra
        self.SemGente = threading.Semaphore(1)

    def clientesEntra(self):
        self.SemGente.acquire()
        # if(self.gente == self.capacidad):
        #     print("ERROR: QUIERE ENTRAR ALGUIEN QUE NO DEBE")
        #     exit()
        self.gente += 1
        self.totalgente += 1
        self.SemGente.release()

    def clienteSale(self):
        self.SemGente.acquire()
        if(self.gente == 0):
            print("ERROR: QUIERE SALIR ALGUIEN QUE NO ESTA DENTRO")
            exit()
        self.gente -= 1
        self.SemGente.release()

    def clientesDentro(self):
        return self.gente

    def estaLLeno(self):
        return self.gente < self.capacidad

    def termino(self):
        self.SemGente.acquire()
        cond = not(self.total == self.totalgente)
        self.SemGente.release()
        return cond


class Clientes(threading.Thread):
    def __init__(self, Satendido, Sclientes, tienda, i):
        threading.Thread.__init__(self)
        self.Satendido = Satendido
        self.Sclientes = Sclientes
        self.tienda = tienda
        self.nombre = "Cliente-" + str(i)  # nombre del cliente

    def run(self):
        # cliente intenta entrar
        self.tienda.clientesEntra()
        # aviso llegue
        self.Sclientes.release()
        # espero pasar
        self.Satendido.acquire()
        print("cliente " + self.nombre + " se corto el pelito")
        sleep(3)
        # se vira
        self.tienda.clienteSale()


class Barbero(threading.Thread):
    def __init__(self, Satendido, Sclientes, tienda):
        threading.Thread.__init__(self)
        self.Satendido = Satendido
        self.tienda = tienda
        self.Sclientes = Sclientes

    def run(self):
        while self.tienda.termino():  # REVISAR condicion de termino

            self.Sclientes.acquire()
            self.Satendido.release()
            # time.sleep(0.25)
            print("estoy cortando el pelito, clientes atendidos: " +
                  str(self.tienda.totalgente))
        print("Termine de atender")
        return
