#!/usr/bin/python

# Peter Barker
# 2017-04-21


from __future__ import print_function

import os
import sys
import util

import mga_tool
from optparse import OptionParser

import ublox.mga.offline

#mgaoffline = mga.MGAOffline(token="bob")
#mgaoffline.make_request()
#sys.exit(1)

class MGAOffline(mga_tool.MGATool):
    def __init__(self):
        pass
    def run(self):
        parser = OptionParser("mga-offline.py")
        parser.add_option("--port", help="serial port", default='/dev/ttyACM0')
        parser.add_option("--baudrate", type='int',
                          help="serial baud rate", default=115200)
#        parser.epilog = "upload: upload to device\ndownload: download from device"
        (opts, args) = parser.parse_args()

        cache = ublox.mga.offline.Offline(cachefile="/tmp/mga-offline.ubx")
        cache.freshen()

tool = MGAOffline()
tool.run()



        self.dev = ublox.UBlox(opts.port, baudrate=opts.baudrate, timeout=2)
        self.configure_dev()

        do_request = False
        if do_request:
            out_fh = open("/tmp/mga-offline.ubx", "w")

            token = "U9cXKihAAkOqBwXwcl5vmA"
            mgaofflinerequester = mga.MGAOfflineRequester(token=token)
            fh = mgaofflinerequester.make_request()
            content = fh.read()
            out_fh.write(content)
            fh.close()

