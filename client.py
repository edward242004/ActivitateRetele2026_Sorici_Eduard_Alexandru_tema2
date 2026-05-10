import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999
BUFFER_SIZE = 1024
TIMEOUT     = 5

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

este_conectat = False

def trimite_comanda(mesaj: str) -> str:
    try:
        client_socket.sendto(mesaj.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
        date_brute, _ = client_socket.recvfrom(BUFFER_SIZE)
        return date_brute.decode('utf-8')
    except socket.timeout:
        return "EROARE: Serverul nu raspunde (timeout)."
    except Exception as e:
        return f"EROARE: {e}"


print("=" * 55)
print("  CLIENT UDP - Seminar 9")
print("=" * 55)
print("  Comenzi disponibile:")
print("    CONNECT              - conectare la server")
print("    DISCONNECT           - deconectare de la server")
print("    PUBLISH <mesaj>      - publicare mesaj")
print("    DELETE <id>          - stergere mesaj dupa ID")
print("    LIST                 - afisare toate mesajele")
print("    EXIT                 - inchidere client")
print("=" * 55)
print()

while True:
    try:
        intrare = input(">> ").strip()
    except (KeyboardInterrupt, EOFError):
        break

    if not intrare:
        continue

    parti = intrare.split(' ', 1)
    comanda = parti[0].upper()
    argumente = parti[1] if len(parti) > 1 else ''

    if comanda == 'EXIT':
        print("Inchidere client...")
        break

    if comanda in ['PUBLISH', 'DELETE', 'LIST', 'DISCONNECT'] and not este_conectat:
        print("EROARE: Trebuie sa te conectezi mai intai (comanda CONNECT).")
        continue

    if comanda == 'CONNECT':
        raspuns = trimite_comanda(intrare)
        print(raspuns)
        if raspuns.startswith("OK"):
            este_conectat = True

    elif comanda == 'DISCONNECT':
        raspuns = trimite_comanda(intrare)
        print(raspuns)
        if raspuns.startswith("OK"):
            este_conectat = False

    elif comanda == 'PUBLISH':
        if not argumente:
            print("EROARE LOCALA: Comanda PUBLISH necesita un mesaj. (ex: PUBLISH Salut)")
            continue
        print(trimite_comanda(intrare))

    elif comanda == 'DELETE':
        if not argumente or not argumente.isdigit():
            print("EROARE LOCALA: Comanda DELETE necesita un ID numeric. (ex: DELETE 1)")
            continue
        print(trimite_comanda(intrare))

    elif comanda == 'LIST':
        print(trimite_comanda(intrare))

    else:
        print(f"Comanda '{comanda}' nu este recunoscuta.")

client_socket.close()
