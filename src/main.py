from tienda import *
import threading


def main():
    cliente = threading.Semaphore()
    cola = threading.Semaphore()
    atendido = threading.Semaphore()
    t1 = Barbero(cola, atendido, cliente)
    clientes = list()
    for i in range(40):
        clientes.append(Clientes(cola, atendido, cliente))
    # START
    for i in range(len(clientes)):
        clientes[i].start()
    t1.start()
    # espero que termine
    for i in range(len(clientes)):
        clientes[i].join()
    t1.join()


if __name__ == "__main__":
    main()
