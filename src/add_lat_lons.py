import typer
import csv
from tempfile import NamedTemporaryFile

cliapp = typer.Typer()

fields = ["WorkplaceName", "AddressLine1", "AddressLine2",
          "AddressLine3", "City", "Region", "Country", "PostalCode", "lat", "lon"]


@cliapp.command()
async def add_locations_to_csv(filename: str):
    apikey_file = open(".gmaps_apikey", "r")
    gmaps_key = apikey_file.read().strip()
    apikey_file.close()
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open(filename, 'r') as rf, tempfile:
        reader = csv.DictReader(rf, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
