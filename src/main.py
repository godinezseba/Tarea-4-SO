from tienda import Tienda, Clientes, Barbero
import threading


def main():
    cliente = threading.Semaphore(0)
    atendido = threading.Semaphore(0)
    tienda = Tienda(40)
    t1 = Barbero(atendido, cliente, tienda)
    clientes = list()
    for i in range(40):
        clientes.append(Clientes(atendido, cliente, tienda, i+1))
    # START
    t1.start()
    for i in range(len(clientes)):
        clientes[i].start()

    # espero que termine
    for i in range(len(clientes)):
        clientes[i].join()
    t1.join()


if __name__ == "__main__":
    main()
