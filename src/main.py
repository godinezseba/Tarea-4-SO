from tienda import Tienda, Clientes, Mesones
import threading


def main():
    cliente = threading.Semaphore(0)
    atendido = threading.Semaphore(0)
    tienda = Tienda(40)
    clientes = list()
    mesones = list()
    # genero los mesones
    for i in range(5):
        mesones.append(Mesones(atendido, cliente, tienda, i+1))
    # genero los clientes:
    for i in range(40):
        clientes.append(Clientes(atendido, cliente, tienda, i+1))
    # START
    for i in range(len(mesones)):
        mesones[i].start()
    for i in range(len(clientes)):
        clientes[i].start()

    # espero que termine

    for i in range(len(clientes)):
        clientes[i].join()
    for i in range(len(mesones)):
        mesones[i].join()

if __name__ == "__main__":
    main()
