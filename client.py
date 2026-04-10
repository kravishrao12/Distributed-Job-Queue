import socket
import ssl

HOST = "10.20.201.112"   # ← your server IP
PORT = 5000

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(sock, server_hostname=HOST)

conn.connect((HOST, PORT))
conn.send("CLIENT".encode())

print("Connected to server.\n")

while True:
    print("\n1.Sum 2.Sub 3.Mul 4.Div 5.Fact 6.Exit")
    choice = input("Enter choice: ")

    if choice == "6":
        break

    if choice in ["1","2","3","4"]:
        a = input("Enter first number: ")
        b = input("Enter second number: ")
        job = f"{choice} {a} {b}"

    elif choice == "5":
        a = input("Enter number: ")
        job = f"{choice} {a}"

    else:
        continue

    conn.send(f"SUBMIT {job}".encode())

    response = conn.recv(1024).decode()
    print("Server:", response)

    result = conn.recv(1024).decode()
    print("Final Result:", result)

conn.close()