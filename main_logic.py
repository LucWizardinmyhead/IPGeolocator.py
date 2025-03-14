# IP ADDRESS GEO LOCATOR // CREATED BY BARI AND LUCAS 



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
import requests, threading, shodan



# FILE IMPORT
from pathlib import Path

# PATH HANDLING
base_dir = Path.home() / "Documents" / "GitHub" / "IPGeolocator.py" 
base_dir.mkdir(parents=True, exist_ok=True)




# START OF LOGIC FOR PULLING GEO INFO // WITH IPINFO
class GeoLookup():
    """This class will be responsible for pulling the geo location of x, using the ipinfo.io api"""

    def __init__(self):
        pass


    def geo_lookup(self, ip):
        """This will handle the request to pull geo information"""

        # INITALIZE THE TABLE
        table = Table(title="IP Info", style="purple")
        table.add_column("Key", style="bold blue")
        table.add_column("Value", style="bold green")
        panel_on = Panel(renderable= f"Geo Lookup for: {ip} Successfully Completed", style="bold green", border_style="bold green", expand=False)


        # CREATE THE URL WITH THE IP
        url = f"https://ipinfo.io/{ip}"
        
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            
            info = response.json()
            
            with Live(table, console=console, refresh_per_second=50):
                for key, value in info.items():
                    
                    # NOW TO APPEND DATE TO THE TABLE
                    table.add_row(f"{key}", f"{value}")

            
            console.print(f"\n{panel_on}")
            
            
        
        else:
            panel_off = Panel(title=f"Geo Lookup for: {ip} Failed, {response.text}", style="bold red", border_style="bold red", expand=False)
            console.print(panel_off)

            error = response.text
            console.print(f"[bold red]Error: {error}[/bold red]")


domain = socket.gethostbyname(input("Enter Domain: "))
GeoLookup().geo_lookup(ip=domain)