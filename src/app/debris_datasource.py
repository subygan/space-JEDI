
class DebrisDataSource:
    # get a dictionary with the TLE data
    # the key should be an unique value for each debris
    def get_updated_tle_data(self, sync_settings):
        raise NotImplementedError()
        