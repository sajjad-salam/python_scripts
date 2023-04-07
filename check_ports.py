
# Set up SSH connection
import paramiko
router_ip = "192.168.1.109"
router_username = "admin"
router_password = "1212qwqw"


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(router_ip, username=router_username, password=router_password)
    print("Connection successful🤍🤍")
except paramiko.AuthenticationException:
    print("Authentication failed!")
except paramiko.SSHException:
    print("Unable to establish SSH connecti")
except paramiko.socket.error as e:
    print(f"Connection error: {e}")

stdin, stdout, stderr = ssh.exec_command('/interface ethernet print detail where name=ether1')
output = stdout.readlines()
port_status = None
for line in output:
    if 'link-ok' in line:
        port_status = True
    elif 'link-down' in line:
        port_status = False

ssh.close()

# # Print port status
if port_status:
    print('Port is up')
else:
    print('Port is down')