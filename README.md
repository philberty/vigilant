Watchy
------

Watchy provides application driven, distributed stats/process/log monitoring. The project is made up of several separate
components the Server with angularjs dashboard, the stats daemon and finally your client applications.

Imagine starting your application as so:

```python
def myApplication()
    ...

import os
import StatsCore

client = StatsCore.attachOrCreateStatsDaemon()
client.postWatchPid('myapplication', os.getpid())
client.close()

myApplication()
```

When you do this this will automatically create or attach to the local daemon on the host server, which in turn does all
process monitoring on that server and relays all data up to the server over a specified transport (udp is currently the
only transport). Once the data hits the server you will see beautiful charts and your data. When your process stops or
crashes the daemon knows and will stop monitoring, but when you start your app up again magic you will have your stats
back again. No need to look up process id's.
