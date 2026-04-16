#!/usr/bin/env python3

import argparse
import json
import os
import sys
import time
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

def parse_args():
    parser = argparse.ArgumentParser(prog="exile",
                                     description="Delay access to a secret")
    parser.add_argument("secret", nargs="?")
    parser.add_argument("-c", "--cancel", action="store_true",
                        help="cancel unlock request")
    parser.add_argument("-d", "--delay", type=int, default=60, 
                        help="delay duration in minutes")
    parser.add_argument("-f", "--force", action="store_true",
                        help="overwrite existing secret")
    parser.add_argument("-r", "--remove", action="store_true")
    return parser.parse_args()

DATA_DIR = Path.home() / ".cache"
DATA_FILE = DATA_DIR / "exile_data"
MASTER_KEY = "REPLACE WITH MASTER KEY"

class Store:
    def __init__(self, key, path):
        self.fernet = Fernet(key)
        self.path = path

    def read(self):
        return json.loads(self.fernet.decrypt(
            self.path.read_bytes()
        ).decode())

    def write(self, obj):
        self.path.write_bytes(
            self.fernet.encrypt(json.dumps(obj).encode())
        )

def main():
    args = parse_args()
    store = Store(MASTER_KEY, DATA_FILE)
    
    if args.secret:
        if store.path.exists() and not args.force:
            print("A secret is already stored. Use '-f' to overwrite")
            return
        
        DATA_DIR.mkdir(exist_ok=True)
        store.write({ "secret": args.secret, "delay": args.delay })
        return

    if not store.path.exists():
        print("No secret is stored")
        return

    if args.remove:
        store.path.unlink()
        return

    data = store.read()

    if args.cancel:
        data.pop("unlock_time", None)
        store.write(data)
        return

    unlock_time = data.get("unlock_time")
    now = time.monotonic()
    if not unlock_time or now - unlock_time < 0:
        data["unlock_time"] = unlock_time = now

    elapsed_seconds = now - unlock_time
    if  elapsed_seconds > data["delay"] * 60:
        print(data["secret"], end='')
        del data["unlock_time"]
    else:
        seconds = int(data["delay"] * 60 - elapsed_seconds)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        print("Secret will be available after", end='')
        if hours:
            print_time(hours, "hour")
        if minutes:
            print_time(minutes, "minute")
        if not hours and not minutes:
            print_time(seconds, "second")
        print()

    store.write(data)

def print_time(amount, unit):
    if amount > 1:
        unit += 's'
    print(f" {amount} {unit}", end='')

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
