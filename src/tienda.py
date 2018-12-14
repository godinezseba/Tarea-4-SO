import threading
from time import sleep


class Tienda():
    def __init__(self, cantidad):
        self.capacidad = 30  # total gente que puede estar dentro
        self.gente = 0  # gente actual dentro de la tienda
        self.total = cantidad  # total de gente a atender
        self.totalgente = 0  # cantidad de gente atendida
        # semaforo para controlar la gente que entra
        self.SemGente = threading.Semaphore(self.capacidad)
        # semaforo para alterar la variable de gente que entra
        self.checkGente = threading.Semaphore(1)

    def clientesEntra(self):
        self.SemGente.acquire()
        self.gente += 1

    def clienteSale(self):
        # actualizo el total
        self.checkGente.acquire()
        self.totalgente += 1
        self.checkGente.release()

        self.gente -= 1
        self.SemGente.release()  # libero para que entre otro

    # funcion de termino para los distintos componentes de la tienda
    # checkea que se hayan atendido todos los clientes esperados

    def termino(self, clientes):
        clientes.acquire()
        print("HOLA")
        self.checkGente.acquire()
        cond = not(self.total == self.totalgente)
        self.checkGente.release()
        return cond

    # nose si las use
    def clientesDentro(self):
        return self.gente

    def estaLLeno(self):
        return self.gente < self.capacidad


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
        print(self.nombre + " fue a la mesa")
        sleep(3)
        # se vira
        # print("---Termino " + self.nombre + "---")
        self.tienda.clienteSale()


class Mesones(threading.Thread):
    def __init__(self, Satendido, Sclientes, tienda, i):
        threading.Thread.__init__(self)
        self.Satendido = Satendido
        self.tienda = tienda
        self.Sclientes = Sclientes
        self.nombre = "Meson-"+str(i)
        self.cantidad = 0

    def run(self):
        # REVISAR condicion de termino
        while (self.tienda.termino(self.Sclientes)):
            self.Satendido.release()
            self.cantidad += 1
            print(self.nombre + " " + str(self.cantidad) + " atendiendo, total clientes atendidos: " +
                  str(self.tienda.totalgente))
        print("***Termine de atender " + self.nombre + "***")
        return
