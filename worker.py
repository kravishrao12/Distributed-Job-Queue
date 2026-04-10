import socket
import ssl
import math
import time
import signal
import sys

HOST = "127.0.0.1"
PORT = 5000

def handle_exit(sig, frame):
    print("\n[WORKER TERMINATED]")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = context.wrap_socket(sock, server_hostname=HOST)

        conn.connect((HOST, PORT))
        conn.send("WORKER".encode())

        job = conn.recv(1024).decode()

        if job == "NO_JOB":
            print("No job available... waiting")
            conn.close()
            time.sleep(2)
            continue

        elif job.startswith("JOB"):
            _, job_id, *parts = job.split()

            print("Received job:", job_id, parts)

            op = parts[0]

            try:
                if op == "1":
                    result = int(parts[1]) + int(parts[2])
                elif op == "2":
                    result = int(parts[1]) - int(parts[2])
                elif op == "3":
                    result = int(parts[1]) * int(parts[2])
                elif op == "4":
                    result = int(parts[1]) / int(parts[2])
                elif op == "5":
                    result = math.factorial(int(parts[1]))
                else:
                    result = "INVALID"
            except:
                result = "ERROR"

            print("Processing job... Press Ctrl+C to simulate failure")
            time.sleep(10)

            conn.send(f"RESULT {job_id} {result}".encode())
            conn.close()

    except Exception as e:
        print("Worker error:", e)
        time.sleep(2)