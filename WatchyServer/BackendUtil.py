import sys
import time
import Queue
import threading
import traceback
import ServerUtil

import WatchyServer.backends.Backend_MongoDB as mongo
import WatchyServer.backends.Backend_RabbitMQ as rabbit

class BackendInitException (Exception):
    pass

def MongoBackendInit (node, config):
    try:
        uri = str (config.get (node, 'uri'))
    except:
        raise BackendInitException ('Invalid uri option for backend mongodb')
    return mongo.Backend_Mongo (uri)

def RabbitBackendInit (node, config):
    try:
        uri = str (config.get (node, 'uri'))
    except:
        raise BackendInitException ('Invalid uri option for backend rabbitmq')
    return rabbit.Backend_Rabbit (uri)

def Backend (node, config):
    try:
        btype = str (config.get (node, 'type'))
    except:
        raise BackendInitException ('Invalid or no type option in config section %s' % node)
    if btype == 'mongodb':
        return MongoBackendInit (node, config)
    if btype == 'rabbitmq':
        return RabbitBackendInit (node, config)
    else:
        raise BackendInitException ('Unknown backend type %s' % btype)

BackendDispatch = Queue.Queue ()
class AsyncBackend (threading.Thread):
    def __init__ (self, backends):
        threading.Thread.__init__ (self)
        self.running = False
        self.backends = backends

    def run (self):
        ServerUtil.info ('Starting Async Backend handler')
        self.running = True
        while self.running:
            try:
                data = BackendDispatch.get (False)
                for i in self.backends:
                    i.consume (data)
            except Queue.Empty:
                time.sleep (1)
            except:
                ServerUtil.error ("%s" % traceback.format_exc ())
                ServerUtil.error ("%s" % sys.exc_info ()[1])
        ServerUtil.info ("Async Backend gacefully exited")
