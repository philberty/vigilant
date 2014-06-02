import pika

class Backend_Rabbit:
    def __init__ (self, uri):
        params = pika.connection.URLParameters (uri)
        self.connection = pika.BlockingConnection (params)
        self.channel = self.connection.channel ()

    def consume (self, key, name, data):
        pass
