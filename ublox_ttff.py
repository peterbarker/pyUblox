#!/usr/bin/python

# Peter Barker
# 2017-04-13

# test a uBlox GPS to see how long it takes to get first fix.  may use
# a script to power-cycle the GPS unit; I use an Arduino sketch to
# toggle a pin which toggles a relay.

import sys
import time

import ublox

class TTFF(object):
    def __init__(self):
        self.state_deathly_cold = 14
        self.state_waiting_for_messages = 15
        self.state_waiting_for_nav_status = 16
        self.state_configuring = 17
        self.state_fix_acquired = 18
        self.state_first_configure = 19
        pass

    def configure_dev(self):
#        self.dev.set_logfile(opts.log, append=opts.append)
        self.dev.set_binary()
        self.dev.configure_poll_port()
#        self.dev.configure_poll(ublox.CLASS_CFG, ublox.MSG_CFG_USB)
#        self.dev.configure_poll(ublox.CLASS_MON, ublox.MSG_MON_HW)
        self.dev.configure_poll(ublox.CLASS_MON, ublox.MSG_MON_VER)
        self.dev.configure_port(port=ublox.PORT_SERIAL1, inMask=1, outMask=1)
#        self.dev.configure_port(port=ublox.PORT_USB, inMask=1, outMask=1)
#        self.dev.configure_port(port=ublox.PORT_SERIAL2, inMask=1, outMask=1)
        self.dev.configure_poll_port()
        self.dev.configure_poll_port(ublox.PORT_SERIAL1)
#        self.dev.configure_poll_port(ublox.PORT_SERIAL2)
#        self.dev.configure_poll_port(ublox.PORT_USB)
        self.dev.configure_solution_rate(rate_ms=1000)

        # self.dev.set_preferred_dynamic_model(opts.dynModel)
        # self.dev.set_preferred_usePPP(opts.usePPP)

        self.dev.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_POSLLH, 1)
        self.dev.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_STATUS, 1)
        self.dev.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_SOL, 0)
        self.dev.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_VELNED, 0)
        self.dev.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_SVINFO, 0)
        self.dev.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_VELECEF, 0)
        self.dev.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_POSECEF, 0)
        self.dev.configure_message_rate(ublox.CLASS_RXM, ublox.MSG_RXM_RAW, 0)
        self.dev.configure_message_rate(ublox.CLASS_RXM, ublox.MSG_RXM_SFRB, 0)
        self.dev.configure_message_rate(ublox.CLASS_RXM, ublox.MSG_RXM_SVSI, 0)
        self.dev.configure_message_rate(ublox.CLASS_RXM, ublox.MSG_RXM_ALM, 0)
        self.dev.configure_message_rate(ublox.CLASS_RXM, ublox.MSG_RXM_EPH, 0)
        self.dev.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_TIMEGPS, 0)
        self.dev.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_CLOCK, 0)
        self.dev.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_DOP, 0)
        self.dev.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_PVT, 0)
        self.dev.configure_poll(ublox.CLASS_CFG, ublox.MSG_CFG_NAVX5)

    def run(self):
        from optparse import OptionParser

        parser = OptionParser("ttff.py")
        parser.add_option("--port", help="serial port", default='/dev/ttyACM0')
        parser.add_option("--baudrate", type='int',
                          help="serial baud rate", default=115200)
        (opts, args) = parser.parse_args()

        self.dev = ublox.UBlox(opts.port, baudrate=opts.baudrate, timeout=2)
        self.state = self.state_deathly_cold

        self.start_time = time.time()
        while self.state != self.state_fix_acquired:
            now = time.time()
            if self.state == self.state_deathly_cold:
                print("resetting module")
                self.dev.module_reset(0xffff, 0x00)
                time.sleep(0.1)
                self.state = self.state_first_configure
                # fall through....
            if self.state == self.state_first_configure:
                self.configure_dev()
                self.state = self.state_configuring
            msg = self.dev.receive_message()
            print("msg: %s" % str(msg))
            if self.state == self.state_configuring:
                if msg is not None:
                    self.state = self.state_waiting_for_nav_status
                else:
                    self.configure_dev()
            if msg is None:
                time.sleep(0.01)
                continue
            if self.state == self.state_waiting_for_nav_status:
                if msg.msg_type() == (ublox.CLASS_NAV, ublox.MSG_NAV_STATUS):
                    print("nav_status")
                    if msg.gpsFix == 0x03:
                        print("3D fix aquired after %u seconds" % (time.time()-self.start_time))
                        print("msg: %s" % (str(msg),))
                        self.state = self.state_fix_acquired
                        continue

            if msg is None:
                time.sleep(0.01)
            print("msg: %s" % str(msg))

ttff = TTFF()
ttff.run()
