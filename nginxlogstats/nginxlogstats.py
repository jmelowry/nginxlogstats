#!/usr/bin/env python

from sys import argv
import logging
import ipaddress
import colorama


LOG_LEVEL = 'DEBUG'

logging.basicConfig(level=logging.DEBUG)


class NginxLogStats:

    def __init__(self, logfile):

        self.logfile = logfile
        self.lf = []

    def load_log(self):
        # this load function assumes an nginx default configuration. 
        # todo: configure log format from the nginx config file

        with open(self.logfile, 'r') as lf:

            for line in lf:

                ip = line.split('-')[0].rstrip()
                timestamp = line.split('[')[1].split(']')[0]
                method = line.split('"')[1].split('"')[0].split(' ')[0]
                location = line.split('"')[1].split(' ')[1]
                response_code = int(line.split('" ')[1].split(' ')[0])

                # Validate IP Address
                try:
                    parsed_ip = ipaddress.ip_address(ip)
                    
                    self.lf.append(
                        [parsed_ip, timestamp, method, location, response_code])

                except ValueError:
                    logging.error(
                        '{0} does not appear to be a valid IP address.'.format(ip))

                # logging.debug(parsed_ip)

                # logging.debug(ip)

    def summarize(self):

        # format of each line is:
        # [ IP address (object), date field (string), http method (string), location (string), response code (int) ]
        for request in self.lf:

            print(request)
        # summary will be output (csv, html, stdout, etc... )
        summary = ""

        return summary

def cli():

    #logfile = argv[1]

    test = NginxLogStats('/Users/jamie/github/nginx-log-stats/sample-logs/sample_access.log')
    test.load_log()
    test.summarize()

    print('cli accessed')


if __name__ == '__main__':

    cli()