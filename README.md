# Distributed Job Queue Service (CN Mini Project)

## Overview

This project implements a distributed job queue system using TCP sockets with SSL encryption. Multiple clients submit jobs, and multiple workers execute them concurrently.

## Features

* TCP socket programming
* SSL/TLS secure communication
* Multi-client and multi-worker support
* Centralized job queue
* Job ID-based tracking (Phase 2)
* Result routing to correct client

## Architecture

Client → Server → Job Queue → Worker → Result → Client

## How to Run

### 1. Generate SSL Certificate

python generate_cert.py

### 2. Start Server

python server.py

### 3. Start Workers

python worker.py

### 4. Run Client

python client.py

## Requirements

* Python 3.x
* cryptography library

## Phase 2 Enhancements

* Job ID tracking
* Structured protocol (SUBMIT / JOB / RESULT)
* Improved reliability and scalability
