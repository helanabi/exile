#!/usr/bin/env python3

import sys
from cryptography.fernet import Fernet

sys.stdout.write(repr(Fernet.generate_key()))
