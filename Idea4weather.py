import socket
import requests
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.console import Console
from rich.text import Text

class GeoLookup:
    def __init__(self):
        self.console = Console()
        self.timeout = 5
        self.endpoints = {
            'geo': 'https://ipinfo.io',
            'weather': 'https://wttr.in'
        }

    def _fetch_data(self, url, params=None):
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.console.print(f"[yellow]Warning: API request failed: {e}[/yellow]")
            return None

    def _get_weather(self, lat, lon):
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

    def _format_location_info(self, info):
        """Format location information for display"""
        location_info = []
        if 'ip' in info:
            location_info.append(("IP Address", info['ip']))
        if 'city' in info and 'region' in info and 'country' in info:
            location = f"{info['city']}, {info['region']}, {info['country']}"
            location_info.append(("Location", location))
        if 'loc' in info:
            location_info.append(("Coordinates", info['loc']))
        if 'org' in info:
            location_info.append(("Organization", info['org']))
        if 'timezone' in info:
            location_info.append(("Timezone", info['timezone']))
        return location_info

    def _create_table(self, info):
        # Create main table
        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=None,
            padding=(0, 2),
            collapse_padding=True
        )
        
        # Add columns
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        # Add location information
        table.add_row("[bold cyan]LOCATION INFORMATION[/bold cyan]", "")
        for prop, value in self._format_location_info(info):
            table.add_row(prop, str(value))

        # Add weather information if available
        if 'weather' in info and info['weather']:
            table.add_row("")  # Empty row for spacing
            table.add_row("[bold cyan]WEATHER INFORMATION[/bold cyan]", "")
            for prop, value in info['weather'].items():
                table.add_row(prop, str(value))

        return table

    def lookup(self, domain):
        try:
            # Get IP from domain
            ip = socket.gethostbyname(domain)
            
            # Get location data
            info = self._fetch_data(f"{self.endpoints['geo']}/{ip}")
            if not info:
                self.console.print("[bold red]Lookup failed[/bold red]")
                return None

            # Add weather data if location is available
            if 'loc' in info:
                lat, lon = info['loc'].split(',')
                weather_data = self._get_weather(lat, lon)
                if weather_data:
                    info["weather"] = weather_data

            # Create and display the table
            table = self._create_table(info)
            
            # Create a panel to contain the table
            panel = Panel(
                table,
                title=f"[bold white]Domain Information: {domain}[/bold white]",
                border_style="blue",
                padding=(1, 2)
            )
            
            # Print the panel
            self.console.print("\n")
            self.console.print(panel)
            self.console.print("\n")
            
            return info

        except socket.gaierror:
            self.console.print("[bold red]Error:[/bold red] Invalid domain name")
        except Exception as e:
            self.console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return None

def main():
    console = Console()
    console.print("\n[bold blue]Domain Information Lookup[/bold blue]")
    console.print("[dim]Enter a domain name to get location and weather details[/dim]\n")
    
    geo_lookup = GeoLookup()
    while True:
        domain = input("\nEnter Domain (or 'quit' to exit): ").strip()
        if domain.lower() == 'quit':
            break
        geo_lookup.lookup(domain)

if __name__ == "__main__":
    main()
    
