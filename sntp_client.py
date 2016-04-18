import ntplib
import time

current_milli_time = lambda: int(round(time.time() * 1000))

def main():
    c = ntplib.NTPClient()
    time.sleep(60)
    for i in range(0,1000):
        try:
            response = c.request('0.pool.ntp.org', version=3)
            print "{0},{1}".format(current_milli_time(),response.offset)
            time.sleep(15)
        except:
            print "Error in SNTP request"

if __name__ == "__main__":
    main()
