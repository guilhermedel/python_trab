from multiprocessing import Process, Array


def writer(shared_message):
    while True:
        msg = input()
        for i in range(len(msg)):
            shared_message[i] = ord(msg[i])
        for i in range(len(msg), len(shared_message)):
            shared_message[i] = 0
        if msg == "sair":
            break


def reader(shared_message):
    while True:
        msg = "".join(
            chr(shared_message[i]) for i in range(len(shared_message))
            if shared_message[i] != 0)
        if msg:
            print(f"Lido: {msg}")
        if msg == "sair":
            break


if __name__ == "__main__":
    shared_message = Array('i', 100)

    p1 = Process(target=writer, args=(shared_message, ))
    p2 = Process(target=reader, args=(shared_message, ))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
