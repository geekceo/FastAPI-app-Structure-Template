import paramiko
from paramiko import ssh_exception
from app.configuration.api_answers import servers_setup
from asyncio import sleep

def set_vpn_user(ip: str, root_pass: str) -> None | Exception:

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, username='root', password=root_pass, port=22)

        channel = client.get_transport().open_session()
        channel.get_pty()
        channel.settimeout(5)
        #channel.exec_command('useradd vpn && $(echo "vpn:lezgivpn" |chpasswd)')
        #channel.settimeout(3)
        command = f'useradd -m vpn \n usermod -aG sudo vpn \n echo "vpn:lezgivpn" | chpasswd \n' +\
            ' echo "vpn ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \n echo "www-data ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \n' +\
            ' chsh -s /bin/bash vpn'
        channel.exec_command(command)
        #channel.exec_command('usermod -aG sudo vpn')
        #channel.exec_command('echo -e "lezgivpn\nlezgivpn" | passwd vpn')
        #channel.exec_command('echo "vpn ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers')
        #print(channel.recv(2048).decode('utf-8').replace('\n', ''))

        channel.close()
        client.close()
    except ssh_exception.BadAuthenticationType:
        return servers_setup.auth_failed_ip
    except ssh_exception.AuthenticationException:
        return servers_setup.auth_failed_pass


def send_config_files(ip: str, root_pass: str):
    transport = paramiko.Transport((ip, 22))
    transport.connect(username='root', password=root_pass)
    sftp = paramiko.SFTPClient.from_transport(transport)

    remotepath = '/home/vpn/openvpn-install.sh'
    localpath = 'C:/Test/openvpn-install.sh'

    #sftp.get(remotepath, localpath)
    sftp.put(localpath, remotepath)

    remotepath = '/home/vpn/setup.sh'
    localpath = 'C:/Test/setup.sh'

    sftp.put(localpath, remotepath)

    sftp.close()
    transport.close()

def configurate_nginx(ip: str, root_pass: str) -> None:

    nginx_conf: str = ''

    with open('C:/Test/nginx_boof.conf', 'r') as f:
        nginx_conf = f.read()


    format_nginx_conf = nginx_conf.replace('ip_addr_here', ip)

    with open('C:/Test/nginx.conf', 'w') as f:
        f.write(format_nginx_conf)

    transport = paramiko.Transport((ip, 22))
    transport.connect(username='root', password=root_pass)
    sftp = paramiko.SFTPClient.from_transport(transport)

    remotepath = '/etc/nginx/nginx.conf'
    localpath = 'C:/Test/nginx.conf'

    sftp.put(localpath, remotepath)

    sftp.close()
    transport.close()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username='root', password=root_pass, port=22)
    channel = client.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(5)
    #channel.exec_command('useradd vpn && $(echo "vpn:lezgivpn" |chpasswd)')
    #channel.settimeout(3)
    command = f'dos2unix /etc/nginx/nginx.conf /etc/nginx/nginx.conf \n sudo service nginx restart \n sudo shutdown -r now'
    channel.exec_command(command)
    #channel.exec_command('usermod -aG sudo vpn')
    #channel.exec_command('echo -e "lezgivpn\nlezgivpn" | passwd vpn')
    #channel.exec_command('echo "vpn ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers')
    #print(channel.recv(2048).decode('utf-8').replace('\n', ''))
    channel.close()
    client.close()


async def configurate_open_vpn(ip: str, root_pass: str) -> None:

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username='vpn', password='lezgivpn', port=22)
    #channel = client.get_transport().open_session()
    #channel.get_pty()
    #channel.settimeout(5)
    #channel.exec_command('useradd vpn && $(echo "vpn:lezgivpn" |chpasswd)')
    #channel.settimeout(3)
    command = f'sudo apt install dos2unix \n sudo chown vpn /home/vpn/setup.sh \n sudo chmod 777 /home/vpn/setup.sh \n' +\
            'sudo chown vpn /home/vpn/openvpn-install.sh \n sudo chmod 777 /home/vpn/openvpn-install.sh \n dos2unix -n setup.sh setup.sh \n' +\
            ' dos2unix -n openvpn-install.sh openvpn-install.sh \n nohup bash /home/vpn/setup.sh >> log.txt &'
    client.exec_command(command)
    #channel.exec_command('usermod -aG sudo vpn')
    #channel.exec_command('echo -e "lezgivpn\nlezgivpn" | passwd vpn')
    #channel.exec_command('echo "vpn ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers')
    #print(channel.recv(2048).decode('utf-8').replace('\n', ''))
    #channel.close()
    client.close()

    await sleep(60)

    configurate_nginx(ip, root_pass)


    
