from multiprocessing import Process, Array, Value, Manager
from datetime import datetime

def reader(shared_message, turn, history):
    while True:
        # Aguarda a vez do leitor
        if turn.value == 0:
            # Lê a mensagem da memória compartilhada
            message = "".join(chr(shared_message[i]) for i in range(len(shared_message)) if shared_message[i] != 0)
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if message and message != "visualizar historico":
                # Armazena a mensagem no histórico
                history.append(f"{timestamp} -> {message}")
                print(f"Lido: {message}")
            if message == "sair":
                break
            turn.value = 1  # Passa a vez para o escritor

if __name__ == "__main__":
    # Criação da memória compartilhada e controle de turno
    shared_message = Array('i', 100)  # Buffer de 100 caracteres
    turn = Value('i', 1)  # 1: vez do escritor, 0: vez do leitor
    manager = Manager()
    history = manager.list()  # Lista compartilhada para armazenar o histórico

    # Criação do processo do leitor
    reader_process = Process(target=reader, args=(shared_message, turn, history))
    reader_process.start()

    while True:
        if turn.value == 1:  # Verifica se é a vez do escritor
            msg = input("Escreva sua mensagem ('sair' para encerrar, 'visualizar historico' para ver o histórico): ")
            if msg == "visualizar historico":
                print("\nHistórico de mensagens:")
                for entry in history:
                    print(entry)
                continue  # Não alterna o turno, permanece com o escritor

            # Escreve a mensagem na memória compartilhada
            for i in range(len(msg)):
                shared_message[i] = ord(msg[i])
            for i in range(len(msg), len(shared_message)):
                shared_message[i] = 0  # Limpa o restante do buffer
            if msg == "sair":
                break
            turn.value = 0  # Passa a vez para o leitor

    # Finaliza o processo do leitor
    reader_process.join()
    print("Conversa encerrada.")
