import paramiko

def set_vpn_user(ip: str, root_pass: str) -> None:

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username='root', password=root_pass, port=22)

    channel = client.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(5)
    #channel.exec_command('useradd vpn && $(echo "vpn:lezgivpn" |chpasswd)')
    #channel.settimeout(3)
    command = f'useradd -m vpn \n usermod -aG sudo vpn \n echo "vpn:lezgivpn" | chpasswd \n' +\
        ' echo "vpn ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers'
    channel.exec_command(command)
    #channel.exec_command('usermod -aG sudo vpn')
    #channel.exec_command('echo -e "lezgivpn\nlezgivpn" | passwd vpn')
    #channel.exec_command('echo "vpn ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers')
    print(channel.recv(2048).decode('utf-8').replace('\n', ''))

    channel.close()
    client.close()