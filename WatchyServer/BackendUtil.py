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
