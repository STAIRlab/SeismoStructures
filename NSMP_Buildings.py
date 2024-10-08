from pathlib import Path
from zipfile import ZipFile
import evnt
from matplotlib import pyplot as plt
import json

# 1) List of `station_codes`

in_dir = Path("buildings/motions_ready")    # set this as the directory where you have saved the zip files

in_patterns = ["[NWP][PR]????", "CE?????"]
station_dirs = []
for i in in_patterns:
    station_dirs.extend(in_dir.glob(i))
station_codes = [station_dir.name for station_dir in station_dirs]
print(station_codes)


# 2) Read the data from the `i`th event of each station
#    and save a figure of the responses.

out_dir = Path("out/")
if not out_dir.exists():
    Path.mkdir(out_dir)

for station in station_codes:
    i = 0                  # set this as the event number of interest
    print(f"Reading station {station}, event {i}")

    events = in_dir.glob(f"{station}/*p.zip")
    event = list(events)[i]
    # with ZipFile(event, "r") as readfile:
    #     if any('.smc' in name for name in readfile.namelist()):
    #         parser = 'smc.read_event'
    #     else:
    #         parser = None

    # event_processed = evnt.read(event)
    # channel_locations = event_processed.motions

    # for motion in event_processed.motions.values():

    fig,ax = plt.subplots()
    for record in evnt.try_zip(event):
        # print(record)
        # location = motion['location_name']
        # direction = component.get('component','?')
        if "type" in record and "accel" in record["type"].lower(): # change .accel to .veloc or .displ as needed
            ax.plot(record.data) #, label=f"{location} - {direction}")

    ax.legend()
    fig.savefig(out_dir/f"{station}_{i}")


# Some stations of interest:
# Berkeley; Great Western Savings -- NSMP Station 1103
# San Francisco; Transamerica Tower -- NSMP Station 1239
# San Francisco; Chevron Bldg; Structure Array 1 -- NSMP Station 1446
# Emeryville; Pacific Park Plaza; Structure Array 1 -- NSMP Station 1662
# CA:SF;New Federal Bld; 1st level -- NSMP Station 1866
# CA:SF; FDIC; 23rd Fl NW side -- NSMP Station 1876
# MO:St Louis;One Bell Ctr -- NSMP Station 2490
# MA:Cambridge;MIT Green Bld 54 -- NSMP Station 2656
# AK:Anchorage;Hilton Hotel -- NSMP Station 2716
# Alhambra; LA County Public Works Hdqtrs -- NSMP Station 0482
# CA Long Beach - VAMC, Bldg 126 -- NSMP Station 5106
# Los Angeles; 1100 Wilshire -- NSMP Station 5233
# Los Angeles; UCLA Factor Bldg -- NSMP Station 5405
# CA:San Diego;US Crthse Annex; 3rd Fl NW -- NSMP Station 5502
# San Francisco - 62-story Resid. Bldg -- CGS - CSMIP Station 58389
# WA:Seattle;Crowne Plaza Hotel -- NSMP Station 7010
# WA:Seattle;New Fed Courthouse -- NSMP Station 7050
# AK:Anchorage;BP Bld -- NSMP Station 8016
# Anchorage - R B Atwood Bldg -- NSMP Station 8040
# Los Angeles; Century City, 2049 CPE -- NSMP Station 0981
# Los Angeles; Century City, 2029 CPE -- NSMP Station 0982
# El Castillo Building -- Puerto Rico UPRM Station B03L

