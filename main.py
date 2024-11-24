from multiprocessing import Process, Array, Value, Manager
from datetime import datetime

def reader(shared_message, turn, history):
    while True:
        # O leitor verifica se é sua vez (turno = 0)
        if turn.value == 0:
            # Lê a mensagem armazenada na memória compartilhada
            message = bytes(shared_message[:]).decode('utf-8').rstrip('\x00')
            # Obtém o timestamp do momento da leitura
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if message and message != "visualizar historico":
                # Adiciona a mensagem ao histórico com o timestamp
                history.append(f"{timestamp} -> {message}")
                print(f"Lido: {message}")
            # Encerra se a mensagem for "sair"
            if message == "sair":
                break
            # Passa o controle para o escritor (turno = 1)
            turn.value = 1

if __name__ == "__main__":
    # Cria a memória compartilhada para as mensagens (buffer de 100 bytes)
    shared_message = Array('b', 100)  # Cada elemento do array representa um byte
    # Controla o turno: 1 para o escritor, 0 para o leitor
    turn = Value('i', 1)
    # Lista compartilhada para armazenar o histórico de mensagens com timestamps
    manager = Manager()
    history = manager.list()

    # Inicia o processo do leitor
    reader_process = Process(target=reader, args=(shared_message, turn, history))
    reader_process.start()

    # Loop principal para o escritor
    while True:
        if turn.value == 1:  # Verifica se é a vez do escritor
            # Solicita ao usuário que escreva uma mensagem
            msg = input("Escreva sua mensagem ('sair' para encerrar, 'visualizar historico' para ver o histórico): ")

            # Se o usuário quiser visualizar o histórico
            if msg == "visualizar historico":
                print("\nHistórico de mensagens:")
                for entry in history:
                    print(entry)
                # Não altera o turno, o escritor continua com o controle
                continue

            # Converte a mensagem para bytes e armazena na memória compartilhada
            encoded_msg = msg.encode('utf-8')
            for i in range(len(encoded_msg)):
                shared_message[i] = encoded_msg[i]
            # Limpa o restante do buffer
            for i in range(len(encoded_msg), len(shared_message)):
                shared_message[i] = 0

            # Encerra o programa se a mensagem for "sair"
            if msg == "sair":
                break

            # Passa o controle para o leitor (turno = 0)
            turn.value = 0

    # Aguarda o término do processo do leitor
    reader_process.join()
    print("Conversa encerrada.")
