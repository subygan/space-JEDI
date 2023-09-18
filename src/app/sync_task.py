import os
from datetime import datetime
import json
import uuid

from tle_file_datasource import TleFileDataSource


CUR_DIR = os.path.dirname(os.path.realpath(__file__))

SETTINGS_FILENAME = os.path.join(CUR_DIR, 'sync-settings.json')

LAST_TLE_MERGED_FILENAME = os.path.join(CUR_DIR, 'datasources', 'last-tle-merged.json')

ERROR_LOG_FILENAME = os.path.join(CUR_DIR, 'error.log')


def log(content):
    try:
        with open(ERROR_LOG_FILENAME, mode='at', encoding='utf-8') as f:
            f.write('\r\n' + content)
    except Exception:
        pass


class SyncTask:
    def __init__(self):
        # create/load settings
        self._create_settings_file()
        settings = {
            'datasources': [],
            'ignore_last_entries': False,
            'download_retries': 3
        }
        with open(SETTINGS_FILENAME, mode='rt', encoding='utf-8') as f:
            settings = { **settings, **json.load(f) }
        with open(SETTINGS_FILENAME, mode='wt', encoding='utf-8') as f:
            f.write(json.dumps(settings, indent=4))
        self.settings = settings

    def run(self):
        data  = { }
        if not self.settings['ignore_last_entries']:
            # load last TLE merged data
            if os.path.exists(LAST_TLE_MERGED_FILENAME):
                with open(LAST_TLE_MERGED_FILENAME, mode='rt', encoding='utf-8') as f:
                    data = { **data, **json.load(f) }

        # get TLE data for each datasource
        for datasource in self.settings['datasources']:
            try:
                if datasource['type'] == 'tle_file':
                    ds = TleFileDataSource(datasource['path'], datasource['local'])
                    data = { **data, **ds.get_updated_tle_data(self.settings) }
                else:
                    raise Exception('Unknow datasource type.')
            except Exception as ex:
                log_content =  datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '  '
                try:
                    log_content += json.dump(datasource, indent=None)
                except Exception:
                    pass
                log_content += '  ' + str(ex)
                log(log_content)

        total = len(data)
        if total > 0:
            # save last merged data
            with open(LAST_TLE_MERGED_FILENAME, mode='wt', encoding='utf-8') as f:
                f.write(json.dumps(data))

            #create a unique filename
            unique_name = uuid.uuid4().hex + '.json'
            new_merged_filename = os.path.join(CUR_DIR, 'datasources', unique_name)

            # create the merged file to serve in the web app
            content = {
                'i': {
                    'd': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    't': total
                },
                'l': [ data[key] for key in data ] # remove keys
            }
            text_content = json.dumps(content, indent=None)

            # save in datasources directory
            with open(new_merged_filename, mode='wt', encoding='utf-8') as f:
                f.write(text_content)

            # save too in api directory
            latest_merged_filename = os.path.join(os.path.dirname(CUR_DIR), 'pub', 'api', 'latest.json')
            with open(latest_merged_filename, mode='wt', encoding='utf-8') as f:
                f.write(text_content)
            

    def _create_settings_file(self):
        if not os.path.exists(SETTINGS_FILENAME):
            content = { }
            text_content = json.dumps(content, indent=None)
            with open(SETTINGS_FILENAME, mode='wt', encoding='utf-8') as f:
                f.write(text_content)
        

if __name__ == '__main__':
    sync_task = SyncTask()
    sync_task.run()
