# UTILITIES MODULE TO  // IP ADDRESS GEO LOCATOR // CREATED BY BARI AND LUCAS 

# UI IMPORTS
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.console import Console
console = Console()
console_width = console.size.width


# NETWORK IMPORTS
from scapy.all import sniff
import socket

# ETC IMPORTS
import requests, threading, shodan, pytz, pyowm
from datetime import datetime



# FILE IMPORT
from pathlib import Path
import json

# PATH HANDLING
base_dir = Path.home() / "Documents" / "GitHub" / "IPGeolocator.py" 
base_dir.mkdir(parents=True, exist_ok=True)


# FOLDER FOR API KEYS
file_api = base_dir / "api_key.json"

class Utilities():
    """This is a class we will use to house get request and etc"""


    def get_time_zone(self, time_zone):
        """This method will be responsible for finding the time of the timezone param"""

        timezone = pytz.timezone(time_zone)
        time = datetime.now(timezone).strftime("%m/%d/%Y - %H:%M:%S")

        console.print(f"[bold blue]Timezone:[/bold blue] [bold red]{time_zone}[/bold red] --> [bold green]{time}[/bold green]")

    
    def get_geo_lookup(self, ip, domain):
        """This will handle the request to pull geo information"""


        # INITALIZE THE TABLE
        table = Table(title="IPInfo.io", style="purple", title_style="bold red", header_style="bold red")
        table.add_column("Key", style="bold blue")
        table.add_column("Value", style="bold green")
        panel_on = Panel(renderable= f"Geo Lookup for: {domain} -->  {ip}  Successfully Completed", style="bold green", border_style="bold green", expand=False)

        
        try:
            # CREATE THE URL WITH THE IP
            url = f"https://ipinfo.io/{ip}"
            
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                
                info = response.json()
                
                with Live(table, console=console, refresh_per_second=50):
                    for key, value in info.items():
                        
                        # NOW TO APPEND DATE TO THE TABLE
                        table.add_row(f"{key}", f"{value}")
                
                console.print(panel_on)
                return info
                    
            else:
                panel_off = Panel(renderable=f"Geo Lookup for: {ip} Failed, {response.text}", style="bold red", border_style="bold red", expand=False)
                console.print(panel_off)

                error = response.text
                console.print(f"[bold red]Error: {error}[/bold red]")
                return False
        
        except Exception as e:
            console.print(e)
            return False
        
        finally:
            print("\n")

    def get_weather(self, lat, lon):
        """Responsible for pulling weather info"""
    
        go = False

        if go:
            try:
                weather_data = self._fetch_data(f"{self.endpoints['weather']}/{lat},{lon}?format=j1")
                
                if not weather_data or 'current_condition' not in weather_data:
                    return None

                current = weather_data['current_condition'][0]
                return {
                    "Temperature": f"{current.get('temp_C', 'N/A')}°C ({current.get('temp_F', 'N/A')}°F)",
                    "Condition": current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
                    "Humidity": f"{current.get('humidity', 'N/A')}%",
                    "Wind Speed": f"{current.get('windspeedKmph', 'N/A')} km/h",
                    "Feels Like": f"{current.get('FeelsLikeC', 'N/A')}°C ({current.get('FeelsLikeF', 'N/A')}°F)"
                }
            
            except Exception as e:
                console.print(e)
        

    def get_ip_info(self, ip):
        """This method will be responsible for pulling information from abuseipdb.com to see if the ip has been reported or marked as malicious"""
        

        # PULL JSON DATA AND STORE IT IN THE DATA VARIABLE
        data = self._get_json_file()


        # CREATE THE OUTPUT TABLE
        table = Table(title="AbuseIPdb.com", style="bold purple", header_style="bold red", title_style="bold red")
        table.add_column("Field", style="bold blue")
        table.add_column("Value", style="bold green")




        if data != False and data["api_key_abuse_ip_db"]:

            # CREATE THE URL WITH THE IP
            url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
            
            # CREATE THE HEADERS WERE WE INCLUDE OUR API KEY

            api_key = data["api_key_abuse_ip_db"]
            
            headers = {
                "key": api_key,
                "Accept": "application/json"
            }

            params = {
                "ipAddress": ip,
                "maxAgeInDays": 365,
                "verbose": "True"
            }

            try:
                response = requests.get(url=url, headers=headers, params=params, timeout=5)
                go = False
                
                # CHECK FOR SUCCESS OR NOT
                if response.status_code == 200:
                    response = response.json() 
        
                 #   info = response["data"]
                    
                    # NOW TO LOOP THROUGH INFO AND OUTPUT INSIDE A TABLE
                    for key, value in response["data"].items():
                        
                        if key.strip().lower() != "reports":
                            table.add_row(f"{key}", f"{value}")
                            go = True
                            
                            
                        # CREATE A SEPERATE TABLE FOR REPORTS
                        else:
                            if response["data"]["reports"]:
                                num = 1
                                for report in response["data"]["reports"]:

                                    # CREATE TABLE FOR REPORTS
                                    table_reports = Table(title=f"Report #{num}", style="white", header_style="bold red", title_style="bold red")
                                    table_reports.add_column("Field", style="bold blue")
                                    table_reports.add_column("Value", style="bold green")
                                    

                                    # ADD INFO INTO THE TABLES
                                    table_reports.add_row(f"reportedAt", f"{report.get("reportedAt", "N/A")}")
                                    table_reports.add_section()
                                    table_reports.add_row("categories", f"{report.get("categories", "N/A")}")
                                    table_reports.add_row("reporterId", f"{report.get("reporterId", "N/A")}")
                                    table_reports.add_row("reporterCountryCode", f"{report.get("reporterCountryCode", "N/A")}")
                                    table_reports.add_section()
                                    table_reports.add_row("comment", f"{ report.get("comment", "N/A")}")

                                    # PRINT RESULTS
                                    console.print(table_reports)
                                    print("\n")
                                    
                                    # INCREASE THE REPORT NUMBER
                                    num += 1

                                    
                    # THIS WILL PRINT VALUES FROM ABUSEIP
                    if go:
                        num -= 1
                        console.print(table)
                        console.print(f"\n[bold green]Abuse Confidence Score of: [/bold green][bold red]{response["data"]["abuseConfidenceScore"]}[/bold red]")
                        console.print(f"[bold green]A Total of:[/bold green] [bold red]{num} reports[/bold red] [bold green]have been found with:[/bold green][bold red] {ip}[/bold red]")
                                

                    #print("\n")
                   # console.print(response)
                
                else:
                    console.print(f"[bold red]Error code: [/bold red]{response.status_code}")

            except Exception as e:
                console.print(e)
        
        else:
            console.print("[bold red]AbuseIPdb query skipped: [/bold red][yellow]no valid api key found[/yellow]")

        print("\n")

    
    def _get_json_file(self):
        """This method is soley for pulling user created json file"""
        
        

        while True:
            
            try:

                if file_api.exists():

                    with open(file_api, "r") as file:
                        content = json.load(file)
                         
                        return content
                
                else:
            
                    data = {
                        "api_key_ipinfo": "",
                        "api_key_abuse_ip_db": "",
                        "api_key_virus_total": ""
                    }

                    with open(file_api, "w") as file:
                        json.dump(data, file, indent=3)

                    console.print(f"[bold blue]Successfully created default json file[/bold blue] - [bold red]{e}[/bold red]")

            except Exception as e:
                console.print(e)
                return False


