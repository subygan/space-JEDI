import requests
import json

url_stations = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"
url_debris_1 = "https://celestrak.org/NORAD/elements/gp.php?GROUP=iridium-33-debris&FORMAT=tle"
url_debris_2 = "https://celestrak.org/NORAD/elements/gp.php?GROUP=cosmos-2251-debris&FORMAT=tle"
url_debris_3 = "https://celestrak.org/NORAD/elements/gp.php?GROUP=1982-092&FORMAT=tle"
url_debris_4 = "https://celestrak.org/NORAD/elements/gp.php?GROUP=1999-025&FORMAT=tle"
url_active_satellites = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

def download_url(url):
	response = requests.get(url)
	tle_data = response.text
	tle_data = [t.strip() for t in tle_data.split("\n")]
	grouped_data = [tle_data[i:i+3] for i in range(0, len(tle_data), 3) if len(tle_data[i:i+3])>2]
	return grouped_data

def download_data():
	stations = download_url(url_stations)
	stations_processed = []
	for i, tle in enumerate(stations):
		tle.append("purple")
		if i==0:
			tle.append("2.5")
		else:
			tle.append("1.5")
		stations_processed.append(tle)

	satellites = download_url(url_active_satellites)
	satellites_processed = []
	for tle in satellites[:400]:
		tle.append("red")
		tle.append("1")
		satellites_processed.append(tle)

	debris_size = 0.5
	N = 1000

	debris_processed = []
	debris = download_url(url_debris_1)
	for tle in debris[:N]:
		tle.append("white")
		tle.append(str(debris_size))
		debris_processed.append(tle)

	debris = download_url(url_debris_2)
	for tle in debris[:N]:
		tle.append("white")
		tle.append(str(debris_size))
		debris_processed.append(tle)


	debris = download_url(url_debris_3)
	for tle in debris[:N]:
		tle.append("white")
		tle.append(str(debris_size))
		debris_processed.append(tle)


	debris = download_url(url_debris_4)
	for tle in debris[:N]:
		tle.append("white")
		tle.append(str(debris_size))
		debris_processed.append(tle)

	all_data = stations_processed + satellites_processed + debris_processed
	json_dump = {"i": {"d": "2023-09-16 01:03:35", "t": len(all_data)}, "l": all_data} 
	with open("latest.json", "w") as f:
		json.dump(json_dump, f)

if __name__ == '__main__':
	download_data()