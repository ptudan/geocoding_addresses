import shutil
import typer
import googlemaps
import csv
from tempfile import NamedTemporaryFile

cliapp = typer.Typer()

fields = [
    "WorkplaceName",
    "AddressLine1",
    "AddressLine2",
    "AddressLine3",
    "City",
    "Region",
    "Country",
    "PostalCode",
    "lat",
    "lon",
]


@cliapp.command()
def add_locations_to_csv(filename: str):
    apikey_file = open(".gmaps_apikey", "r")
    gmaps_key = apikey_file.read().strip()
    apikey_file.close()
    gmaps = googlemaps.Client(key=gmaps_key)
    tempfile = NamedTemporaryFile(mode="w", delete=False)
    with open(filename, "r") as rf, tempfile:
        reader = csv.DictReader(rf, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row["lat"] is None or row["lat"] == "":
                print("adding lat/lon for address: ", row)
                addr = (
                    row["AddressLine1"],
                    row["AddressLine2"],
                    row["AddressLine3"],
                    row["City"],
                    row["Region"],
                    row["PostalCode"],
                    row["Country"],
                )
                geocode_result = gmaps.geocode(",".join(addr))
                if len(geocode_result) == 0:
                    raise Exception("No geocode result found for ", row)
                elif len(geocode_result) > 1:
                    raise Exception("Multiple geocode results found for ", row)
                geocode_result = geocode_result[0]
                print(geocode_result)
                row = {
                    "WorkplaceName": row["WorkplaceName"],
                    "AddressLine1": row["AddressLine1"],
                    "AddressLine2": row["AddressLine2"],
                    "AddressLine3": row["AddressLine3"],
                    "City": row["City"],
                    "Region": row["Region"],
                    "PostalCode": row["PostalCode"],
                    "Country": row["Country"],
                    "lat": geocode_result["geometry"]["location"]["lat"],
                    "lon": geocode_result["geometry"]["location"]["lng"],
                }
            else:
                row = {
                    "WorkplaceName": row["WorkplaceName"],
                    "AddressLine1": row["AddressLine1"],
                    "AddressLine2": row["AddressLine2"],
                    "AddressLine3": row["AddressLine3"],
                    "City": row["City"],
                    "Region": row["Region"],
                    "PostalCode": row["PostalCode"],
                    "Country": row["Country"],
                    "lat": row["lat"],
                    "lon": row["lon"],
                }
            print(row)
            writer.writerow(row)
    shutil.move(tempfile.name, filename)


if __name__ == "__main__":
    cliapp()
