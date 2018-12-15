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
        # semaforo espera caja, izquierda = cliente, derecha =  caja
        self.SemCaja = (threading.Semaphore(0), threading.Semaphore(0)) 
        # semaforo espera mesa, izquierda = cliente, derecha = mesa
        self.SemMesa = (threading.Semaphore(0), threading.Semaphore(0))
     

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
        if self.termino():
            self.SemCaja[1].release()
            self.SemMesa[1].release()

    def pasarCaja(self, nombre):
        self.SemCaja[1].release() # indicar a la caja que llegue
        self.SemCaja[0].acquire() # esperar ser atendido
        print(nombre + " fue a la caja")
        sleep(5)

    def pasarMeson(self, nombre):
        self.SemMesa[1].release()
        self.SemMesa[0].acquire()
        print(nombre + " fue a la meson")
        sleep(3)

    def esperaCaja(self):
        self.SemCaja[1].acquire()
        self.SemCaja[0].release()
    
    def esperaMeson(self):
        self.SemMesa[1].acquire()
        self.SemMesa[0].release()

    # funcion de termino para los distintos componentes de la tienda
    # checkea que se hayan atendido todos los clientes esperados

    def termino(self):
        self.checkGente.acquire()
        cond = self.total == self.totalgente
        self.checkGente.release()
        return cond



class Clientes(threading.Thread):
    def __init__(self, tienda, i):
        threading.Thread.__init__(self)
        self.tienda = tienda
        self.nombre = "Cliente-" + str(i)  # nombre del cliente

    def run(self):
        # cliente intenta entrar
        self.tienda.clientesEntra()
        # va al meson
        self.tienda.pasarMeson(self.nombre)
        # va a la caja
        self.tienda.pasarCaja(self.nombre)
        # se vira
        print("---Termino " + self.nombre + "---")
        self.tienda.clienteSale()


class Mesones(threading.Thread):
    def __init__(self, tienda, i):
        threading.Thread.__init__(self)
        self.tienda = tienda
        self.nombre = "Meson-" + str(i)
        self.cantidad = 0

    def run(self):
        # REVISAR condicion de termino
        while (True):
            self.tienda.esperaMeson()
            if(self.tienda.termino()):
                break
            self.cantidad += 1
            print("\x1b[31m" + self.nombre + " atendiendo " + str(self.cantidad) + "\x1b[0m")
        self.tienda.SemMesa[1].release()
        print("\x1b[31m***Termine de atender " + self.nombre + "***\x1b[0m")


class Cajas(threading.Thread):
    def __init__(self, tienda, i):
        threading.Thread.__init__(self)
        self.tienda = tienda
        self.nombre = "Caja-" + str(i)
        self.cantidad = 0

    def run(self):
        while (True):
            self.tienda.esperaCaja()
            if(self.tienda.termino()):
                break
            self.cantidad += 1
            print("\x1b[32m" + self.nombre + " atendido " + str(self.cantidad) + "\x1b[0m")
        self.tienda.SemCaja[1].release()
        print("\x1b[32m***Termine de atender " + self.nombre + "***\x1b[0m")
