import machine

import utime as time
import ujson as json

import mywifi
import mytz

from mysegdisplay import MySegDisplay


with open('config.json') as configfile:
    CONFIG = json.load(configfile)


def init_display():
    ''' Init and return display object '''
    # Setup I2C Bus for Display/Sensors
    I2C_BUS = machine.I2C(
        scl=machine.Pin(5),
        sda=machine.Pin(4),
        freq=100000)

    print(("I2C Devices Found: {}".format(
        [hex(tmp) for tmp in I2C_BUS.scan()])))

    if len(I2C_BUS.scan()) > 10:
        print("I2C Bus Error. Might be disconnected, please check cable")

    # Configure Display Object
    disp = MySegDisplay(I2C_BUS)

    return disp


def init():
    ''' Init and Connect to WIFI and set RTC from NTP '''
    mywifi.init(CONFIG['wifi'])
    mytz.updatentp(CONFIG['ntp_server'])


def main():

    disp = init_display()
    disp.segtest()

    # Init Wifi, RTC, etc
    init()

    # Loop forever because it crashes otherwise due to Timers it seems
    idx = 0

    while True:
        try:
            start = time.ticks_ms()
            print((mytz.mktime()))

            disp.text(mytz.mkclock(CONFIG['clock']))

            #disp.display(idx)
            #disp.set_digit(0, idx)
            #disp.set_digit(1, idx)
            #disp.set_digit(2, idx)
            #disp.set_digit(3, idx)

            idx += 1

            if idx % 600 == 0:
                mytz.updatentp(CONFIG['ntp_server'])
                idx = 0

            end = time.ticks_ms()
            diff = time.ticks_diff(end, start)

            if diff <= 1000:
                time.sleep((1000 - diff) / 1000)

        except KeyboardInterrupt:
            break

        except Exception as ex:
            print(("Encountered error: %s, re-initializing" % ex))
            try:
                disp.text("88:88")
            except:
                pass
            time.sleep(10)
            machine.reset()


if __name__ == '__main__':
    main()