import sys
import json
import socket
import select
import logging
import threading
import traceback


class UDPStatsServer(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.running = False
        self.daemon = True
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.setblocking(0)

    def run(self):
        logging.info("Starting StatsAggregator on %s:%s" % (self.host, self.port))
        self.serverSocket.bind((self.host, self.port))
        self.running = True
        inputs = [self.serverSocket]
        try:
            while len(inputs) > 0 and self.running is True:
                (reads, writes, errors) = select.select(
                    inputs, [], inputs
                )
                for i in reads:
                    packet = i.recvfrom(256)
                    stats = packet[0].strip().rstrip('\0')
                    try:
                        stat = json.loads(stats)
                        stat['host'] = {'host': packet[1][0], 'port': packet[1][1]}
                        logging.debug("Received [%s] from [%s:%i] for [%s]" % (
                            stat['type'],
                            stat['host']['host'],
                            stat['host']['port'],
                            stat['name']))
                    except:
                        logging.debug("%s" % traceback.format_exc())
                        logging.error("%s" % sys.exc_info()[1])
        except KeyboardInterrupt:
            logging.info("Caught Keyboard interrupt closing")
        finally:
            self.serverSocket.close()
            logging.info("Stats Aggregator exited gracefully")