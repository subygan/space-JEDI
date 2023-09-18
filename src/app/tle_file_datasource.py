import os
from datetime import datetime
import requests
import hashlib
import json

import urllib3
# disable insecure request warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from debris_datasource import DebrisDataSource


CUR_DIR = os.path.dirname(os.path.realpath(__file__))

HISTORY_FILENAME = os.path.join(CUR_DIR, 'datasources', 'tle_datasource_history.json')


class TleFileDataSource(DebrisDataSource):
    def __init__(self, url_or_filename, local=False):
        self.url_or_filename = url_or_filename
        self.local = local
    
    def get_updated_tle_data(self, sync_settings):
        data = { }            

        # get history data 
        self._create_history_file()        
        history = { }
        with open(HISTORY_FILENAME, mode='rt', encoding='utf-8') as f:
            history = { **history, **json.load(f) }
        with open(HISTORY_FILENAME, mode='wt', encoding='utf-8') as f:
            f.write(json.dumps(history, indent=4))
        
        # get file content
        bytes_file = self._get_file(sync_settings)

        # get hash of file
        sha256_hash = hashlib.sha256()
        sha256_hash.update(bytes_file)
        file_hash = sha256_hash.hexdigest()

        # validate if exists
        if not file_hash in history:
            # merge TLE data
            data = { **data, **self._get_tle_data(bytes_file) }

            filename = file_hash + '.txt'
            # save in datasources directory
            with open(os.path.join(CUR_DIR, 'datasources', filename), mode='wb') as f:
                f.write(bytes_file)

            # add to history
            history[file_hash] = {
                'filename': filename,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            # save history file
            with open(HISTORY_FILENAME, mode='wt', encoding='utf-8') as f:
                f.write(json.dumps(history, indent=4))

        return data

    # create a history file if not exists
    def _create_history_file(self):
        if not os.path.exists(HISTORY_FILENAME):
            os.makedirs(os.path.dirname(HISTORY_FILENAME), exist_ok=True)
            content = { }
            with open(HISTORY_FILENAME, mode='wt', encoding='utf-8') as f:
                f.write(json.dumps(content))

    # get the bytes from the file
    def _get_file(self, sync_settings):
        if self.local:
            filename = os.path.join(CUR_DIR, 'datasources', self.url_or_filename)
            if os.path.exists(filename):
                data = None
                with open(filename, mode='rb') as f:
                    data = f.read()
                return data
            else:
                raise FileNotFoundError(filename)
        else:
            for i in range(max(sync_settings['download_retries'], 2)):
                try:
                    response = requests.get(self.url_or_filename, stream=True, verify=False)
                    return response.content
                except Exception:
                    pass
            raise RuntimeError('Error downloading file.')

    # get a dict with TLE data
    # a unique key for each debris
    def _get_tle_data(self, bytes_file: bytes):
        data = { }

        name = None
        tle1 = None
        tle2 = None
        for line in bytes_file.decode('utf-8').splitlines():
            if len(line) == 0:
                continue

            if name is None:
                name = line.strip()
            elif tle1 is None:
                tle1 = line.strip()
            else:
                tle2 = line.strip()

                # using TLE as key
                data[tle1 + tle2] = [ name, tle1, tle2 ]
                
                name = None
                tle1 = None
                tle2 = None

        return data
        