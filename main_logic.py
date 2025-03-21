# IP ADDRESS GEO LOCATOR // CREATED BY BARI AND LUCAS 



# OTHER MODULE IMPORTS
from Utilities import Utilities


# UI IMPORTS
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.console import Console
console = Console()


# NETWORK IMPORTS
from scapy.all import sniff
import socket


# ETC IMPORTS
import requests, threading, shodan, pytz
from datetime import datetime



# FILE IMPORT
from pathlib import Path

# PATH HANDLING
base_dir = Path.home() / "Documents" / "GitHub" / "IPGeolocator.py" 
base_dir.mkdir(parents=True, exist_ok=True)




# START OF LOGIC FOR PULLING GEO INFO // WITH IPINFO
class IPLookup():
    """This class will be responsible for pulling the geo location of x, using the ipinfo.io api"""

    def __init__(self):
        pass

               

    def pull_info(self, ip, domain):
            """This method is used to pull info from all the api's used"""
            
            print("\n")

            # PULL BASIC INFO // PULL GEO INFO
            info = Utilities().get_geo_lookup(ip, domain)

            if info["ip"] != "0.0.0.0":
        
                # PULL WEATHER INFO
                weather = Utilities().get_weather(info["city"], info["country"])

                # PULL IP INFO
                Utilities().get_ip_info(ip)   

                # PULL TIMEZONE
                Utilities().get_time_zone(info["timezone"]  )
            

   
            
            print("\n")
            

    def pull_ip(self):
        """Reverse lookup from domain to ip address"""
        
        while True:
            try:

                domain = console.input("[bold green]Enter Domain or IP:[/bold green] ")

                ip = socket.gethostbyname(domain)
                
                return ip, domain

            
            except Exception as e:
                console.print(f"[bold red]Unexpected Error:[/bold red] [yellow]{e}[/yellow]")
    

    def main(self):
        """The start of greatness"""

        ip, domain = self.pull_ip()
        
        self.pull_info(ip, domain)






IPLookup().main()


