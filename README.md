# Distributed Job Queue Service (CN Mini Project)

## 📌 Overview

This project implements a distributed job queue system using TCP sockets with SSL/TLS encryption. Multiple clients can submit jobs, and multiple worker nodes process them concurrently. The system ensures reliable execution with job tracking and basic fault tolerance.

---

## ⚙️ Architecture

Client → Server → Job Queue → Worker → Server → Client

* **Client**: Submits jobs and receives results
* **Server**: Central coordinator managing job queue and worker assignment
* **Worker**: Executes jobs and returns results

---

## 🔐 Features

* TCP socket-based communication
* SSL/TLS secure communication
* Multi-client and multi-worker support
* Centralized job queue with synchronization
* **Job ID tracking (Phase 2)**
* **Structured communication protocol**
* **Fault tolerance (worker failure handling with requeue)**
* Continuous worker polling
* Scalable design

---

## 🔄 Protocol Design

```
CLIENT → SERVER
SUBMIT <job>

SERVER → WORKER
JOB <job_id> <task>

WORKER → SERVER
RESULT <job_id> <result>

SERVER → CLIENT
RESULT <job_id> <result>
```

---

## 🔢 Supported Operations

| Code | Operation      | Example    |
| ---- | -------------- | ---------- |
| 1    | Addition       | 1 5 7 → 12 |
| 2    | Subtraction    | 2 10 3 → 7 |
| 3    | Multiplication | 3 4 6 → 24 |
| 4    | Division       | 4 20 5 → 4 |
| 5    | Factorial      | 5 6 → 720  |

---

## 🚀 How to Run

### 1. Generate SSL Certificates

```bash
python generate_cert.py
```

### 2. Start Server

```bash
python server.py
```

### 3. Start Workers (multiple)

```bash
python worker.py
```

### 4. Run Client

```bash
python client.py
```

---

## ⚡ Phase 1 vs Phase 2

### Phase 1

* Basic job queue
* Simple client-server communication
* No job tracking

### Phase 2 (Current)

* Job ID tracking (JOB1, JOB2, ...)
* Structured protocol
* Result routing to correct client
* Worker failure handling (requeue)
* Continuous worker polling
* Improved scalability

---

## 💥 Failure Handling

* Worker failure simulated using **Ctrl + C**
* Server detects failure and requeues job
* Another worker completes the job

---

## 📊 Performance & Scalability

* Supports multiple clients and workers
* Increasing workers improves throughput
* Queue ensures load balancing

---

## 🧠 Key Concepts Used

* Distributed Systems
* TCP Socket Programming
* SSL/TLS Encryption
* Multithreading
* Synchronization (Locks)
* Fault Tolerance

---

## ⚠️ Notes

* Do not share `server.key` (private key)
* Works best when client and server are on same network
* Use hotspot if college WiFi blocks connections

---

## 🏁 Conclusion

This project demonstrates a scalable and secure distributed job processing system with job tracking, concurrency, and basic fault tolerance, similar to real-world task scheduling systems.

---
