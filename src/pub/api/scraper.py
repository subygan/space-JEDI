import requests

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
	for tle in stations:
		

if __name__ == '__main__':
	download_data()