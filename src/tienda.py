import threading
from time import sleep
from datetime import datetime

class Baño:
    def __init__(self):
        self.BañoOcupado = threading.Semaphore(1)
        self.ocupado = False
    def Entrar(self):
        self.BañoOcupado.acquire()
        if self.ocupado:
            self.BañoOcupado.release()
            return False
        else:
            self.ocupado = True
            self.BañoOcupado.release()
            sleep(2)
            self.BañoOcupado.acquire()
            self.ocupado = False
            self.BañoOcupado.release()
            return True

class Tienda():
    def __init__(self, cantidad):
        self.capacidad = 30  # total gente que puede estar dentro
        self.gente = 0  # gente actual dentro de la tienda
        self.total = cantidad  # total de gente a atender
        self.totalgente = 0  # cantidad de gente atendida
        self.baño = Baño()
        # semaforo para controlar la gente que entra
        self.SemGente = threading.Semaphore(self.capacidad)
        # semaforo para alterar la variable de gente que entra
        self.checkGente = threading.Semaphore(1)
        # semaforo espera caja, izquierda = cliente, derecha =  caja
        self.SemCaja = (threading.Semaphore(0), threading.Semaphore(0)) 
        # semaforo espera mesa, izquierda = cliente, derecha = mesa
        self.SemMesa = (threading.Semaphore(0), threading.Semaphore(0))
        # semaforo para escribir en el archivo
        self.EscribirC = threading.Semaphore(1)
        self.EscribirF = threading.Semaphore(1)
     

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
        self.EscribirCliente(nombre + " fue a la caja")
        sleep(5)

    def pasarMeson(self, nombre):
        self.SemMesa[1].release()
        self.SemMesa[0].acquire()
        self.EscribirCliente(nombre + " fue al meson")
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

    def EscribirCliente(self, mensaje):
        self.EscribirC.acquire()
        file = open("clientes.txt", 'a')
        file.write("[" + str(datetime.now().time()) + "]" + mensaje + "\n")
        file.close()
        self.EscribirC.release()

    def EscribirFuncionario(self, mensaje):
        self.EscribirF.acquire()
        file = open("funcionarios.txt", 'a')
        file.write("[" + str(datetime.now().time()) + "]" + mensaje + "\n")
        file.close()
        self.EscribirF.release()

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
        self.baño = 0

    def run(self):
        while (True):
            self.tienda.esperaMeson()
            if(self.tienda.termino()):
                break
            self.baño += 1
            self.tienda.EscribirFuncionario(self.nombre + " atendiendo")
            sleep(3)
            if(self.baño >= 4 and self.tienda.baño.Entrar()):
                self.baño = 0
                self.tienda.EscribirFuncionario(self.nombre + " fue al baño")

        self.tienda.SemMesa[1].release() # aviso al resto de mesones para que terminen
        print("\x1b[31m***Termine de atender " + self.nombre + "***\x1b[0m")


class Cajas(threading.Thread):
    def __init__(self, tienda, i):
        threading.Thread.__init__(self)
        self.tienda = tienda
        self.nombre = "Caja-" + str(i)
        self.baño = 0

    def run(self):
        while (True):
            self.tienda.esperaCaja()
            if(self.tienda.termino()):
                break
            self.baño += 1
            self.tienda.EscribirFuncionario(self.nombre + " atendiendo")
            sleep(5)
            if(self.baño >= 5 and self.tienda.baño.Entrar()):
                self.baño = 0
                self.tienda.EscribirFuncionario(self.nombre + " fue al baño")
        self.tienda.SemCaja[1].release() # avso al resto de cajas para que terminen
        print("\x1b[33m***Termine de atender " + self.nombre + "***\x1b[0m")
