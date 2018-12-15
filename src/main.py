from tienda import Tienda, Clientes, Mesones, Cajas
import threading


def main():
    cantidad = 40
    # reseteo los archivos
    clientes = open("clientes.txt", 'w')
    clientes.close()
    funcionarios = open("funcionarios.txt", 'w')
    funcionarios.close()
    # creo la tienda que en su interior tendra los semaforos
    tienda = Tienda(cantidad)
    # creo las hebras
    clientes = list()
    mesones = list()
    cajas = list()
    # genero los mesones
    for i in range(5):
        mesones.append(Mesones(tienda, i+1))
    # genero los cajas
    for i in range(2):
        cajas.append(Cajas(tienda, i+1))
    # genero los clientes:
    for i in range(cantidad):
        clientes.append(Clientes(tienda, i+1))

    # START

    for i in range(len(mesones)):
        mesones[i].start()
    for i in range(len(cajas)):
        cajas[i].start()
    for i in range(len(clientes)):
        clientes[i].start()

    # espero que termine

    for i in range(len(clientes)):
        clientes[i].join()
    for i in range(len(cajas)):
        cajas[i].join()
    for i in range(len(mesones)):
        mesones[i].join()

    print("\x1b[31mLA TIENDA CERRO\x1b[0m")


main()
