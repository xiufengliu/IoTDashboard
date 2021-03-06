# coding: utf-8


from influxdb import DataFrameClient
from influxdb.client import InfluxDBClientError


class InfluxTSDB:
    def __init__(self, dbhost='localhost', dbport=8086, dbuser='root', dbpassword='root', dbname='test'):
        if dbhost != None:
            self.influxdb = DataFrameClient(dbhost, dbport, dbuser, dbpassword, dbname)
            self.dbname = dbname


    def drop_db(self):
        try:
            self.influxdb.drop_database(self.dbname)
        except InfluxDBClientError, e:
            if str(e) == "database does not exist!":
                return True
        return False

    def ensure_db(self):
        try:
            self.influxdb.create_database(self.dbname)
        except InfluxDBClientError, e:
            if str(e) == "database already exists":
                return True
        return False

    def check_ts(self, series_name, prop='*'):
        q = 'select %s from \"%s\" limit 1;' % (prop, series_name)
        result = self.influxdb.query(q)
        return result[series_name].index[0]

    def get_ts(self, series_name, prop='*'):
        q = 'select %s from \"%s\" order by time asc;' % (prop, series_name)
        result = self.influxdb.query(q)
        return result[series_name]

    def get_last_timestamp(self, series_name, prop='*'):
        q = 'select %s from \"%s\" order by time desc limit 1;' % (prop, series_name)
        result = self.influxdb.query(q)
        return result[series_name].index[0]

    def write_ts(self, series_name, df):
        try:
            return self.influxdb.write_points(df, series_name)
        except InfluxDBClientError, e:
            print 'Writing error of InfluxDB '


