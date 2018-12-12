from tienda import *
import threading

cliente = threading.Semaphore()
cola = threading.Semaphore()
atendido = threading.Semaphore()
gente = 0
t1 = Barbero(cola, atendido, cliente)
t2 = Clientes(cola, atendido, cliente, gente)

t1.start()
t2.start()
t1.join()
t2.join()
