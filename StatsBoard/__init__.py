import sys
import logging
import traceback

from . import BoardApp


class StatsBoardServer:
    def __init__(self, bind, port):
        self._bind = bind
        self._port = port

    def listen(self):
        try:
            logging.info('[Flask] starting http://%s:%i/' % (self._bind, self._port))
            BoardApp.app.run(host=self._bind, port=self._port)
        except KeyboardInterrupt:
            logging.warning('Caught keyboard interrupt stopping')
        except:
            logging.error("%s" % traceback.format_exc())
            logging.error("%s" % sys.exc_info()[1])