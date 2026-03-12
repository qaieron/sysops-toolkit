import socket
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("--host", required=True) 
parser.add_argument("--ports", required=True) 
args = parser.parse_args()

args.ports = args.ports.split(",")
int_ports = [int(port) for port in args.ports]

def check_port(host, port, timeout=2):
    start = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            elapsed = (time.time() - start) * 1000
            return True, round(elapsed, 1), None
    except socket.gaierror:
        return False, None, "Host not found"
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False, None, None

for port in int_ports:
    result = check_port(args.host, port)
    if result[2]:
        print(f"{args.host}:{port} - {result[2]}")
        break
    if result[0]:
        print(f"{args.host}:{port} - open ({result[1]}ms)")
    if result[1] is None:
        print(f"{args.host}:{port} - closed")




