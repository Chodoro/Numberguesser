import socket
import random

def generate_secret_number(difficulty):
    if difficulty == "easy":
        return random.randint(1, 50)
    elif difficulty == "medium":
        return random.randint(1, 100)
    elif difficulty == "insane":
        return random.randint(1, 500)
    else:
        return None

def handle_client(conn, addr):
    print(f"Connected to {addr}")

    conn.sendall(b"Welcome to Guess the Number!\n")
    conn.sendall(b"Choose the difficulty level (easy, medium, insane): ")
    difficulty = conn.recv(1024).strip().decode()

    secret_number = generate_secret_number(difficulty)
    if secret_number is None:
        conn.sendall(b"Invalid difficulty level. Please choose from 'easy', 'medium', or 'insane'.\n")
        conn.close()
        return

    attempts = 0

    while True:
        conn.sendall(f"Enter your guess (between 1 and {secret_number}): ".encode())
        guess = int(conn.recv(1024).strip().decode())
        attempts += 1

        if guess < secret_number:
            conn.sendall(b"Too low! Try again.\n")
        elif guess > secret_number:
            conn.sendall(b"Too high! Try again.\n")
        else:
            conn.sendall(f"Congratulations! You've guessed the number {secret_number} in {attempts} attempts!\n".encode())
            break

    conn.close()
    print(f"Connection with {addr} closed")

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            handle_client(conn, addr)

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 12345
    start_server(HOST, PORT)
