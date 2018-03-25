#BAM!
#scriptu' asta ia de la al 2-lea argument un nume de host
#daca nu, ia domain.cfg un nume de host
#daca nu, by default o sa fie gandalf.ru
#dupa, ia de pe fenrir ipu' serverului meu
#si updateaza file-u' cu hosturi din windows
#ez
import sys
import ctypes
import os
from shutil import copyfile
import requests

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_admin():
    script = os.path.abspath(sys.argv[0])
    params = " ".join([script] + sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

if not is_admin():
    get_admin()
    sys.exit()

hosts_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"
tmp_bufer_path = ".\\bufer"
str_serv_ip = requests.get("http://students.info.uaic.ro/~vlad.vatamanu/servip").text

if "not found" in str_serv_ip.lower():
    ctypes.windll.user32.MessageBoxW(None, "N-am gasit adresa IP, Si Fu. Servo non est respondens. :(", "abis", 0)
    sys.exit()

if len(sys.argv) != 2:
    try:
        file_domain = open("domain.cfg", "r")
        str_domain = file_domain.read().strip()
        file_domain.close()
    except FileNotFoundError:
        str_domain = "gandalf.ru"
else:
    str_domain = sys.argv[1]


file_hosts = open(hosts_path)
contents = file_hosts.readlines()
file_hosts.close()

output = ""
for line in contents:
    if str_domain in line:
        continue;

    output += line

output += "{0} {1}\n".format(str_serv_ip.strip(), str_domain)

file_tmp = open(tmp_bufer_path, "w")
file_tmp.write(output)
file_tmp.close()

copyfile(tmp_bufer_path, hosts_path)
os.remove(tmp_bufer_path)
