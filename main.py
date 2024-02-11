import socket
import threading
import re
import time
import random

from DNSServer import DNSServer


b = DNSServer()
b.listen_clients()