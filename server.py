import socket
import ssl
import threading
from jobs_queue import JobQueue

HOST = "0.0.0.0"
PORT = 5000

job_queue = JobQueue()

job_counter = 1
lock = threading.Lock()


def handle_client(conn, addr):
    global job_counter

    print("[CLIENT CONNECTED]", addr)

    data = conn.recv(1024).decode()

    if data.startswith("SUBMIT"):
        job = data.split(" ", 1)[1]

        with lock:
            job_id = f"JOB{job_counter}"
            job_counter += 1

        job_queue.add_job(job_id, job, conn)

        print(f"[JOB RECEIVED] {job_id}: {job}")

        conn.send(f"JOB_ID {job_id}".encode())


def handle_worker(conn, addr):
    print("[WORKER CONNECTED]", addr)

    job_data = job_queue.get_job()

    if job_data:
        job_id, job, client_conn = job_data

        conn.send(f"JOB {job_id} {job}".encode())

        try:
            data = conn.recv(1024).decode()

            if not data:
                raise Exception("Worker disconnected")

            _, r_id, result = data.split(" ", 2)

            print(f"[RESULT] {r_id}: {result}")

            client_conn.send(f"RESULT {r_id} {result}".encode())
            client_conn.close()

            job_queue.complete_job(r_id)

        except Exception:
            print(f"[FAILURE] Worker failed on {job_id}")

            # Requeue job
            job_queue.add_job(job_id, job, client_conn)

    else:
        conn.send("NO_JOB".encode())

    conn.close()


def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    print("[SERVER STARTED WITH SSL]")

    while True:
        client_socket, addr = sock.accept()
        conn = context.wrap_socket(client_socket, server_side=True)

        role = conn.recv(1024).decode()

        if role == "CLIENT":
            threading.Thread(target=handle_client, args=(conn, addr)).start()
        else:
            threading.Thread(target=handle_worker, args=(conn, addr)).start()


if __name__ == "__main__":
    main()