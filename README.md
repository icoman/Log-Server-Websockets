# Logserver with Websokets

A webserver with a logserver running in a thread written in [Python](https://www.python.org/) - [blog announcement](http://rainbowheart.ro/501).

The webserver provide index page with links to each channel from logserver.

Clients connected to webserver receive logs in realtime by websokets.

I made this server when I was bored in a production factory with no Internet access (that was boring) as a test, as a proof of concept.

Feel free to change it and adapt it for your needs.

The webserver starts on port 8080 and also start in a new thread the logserver on 7000.

![Webserver with logserver](http://rainbowheart.ro/static/uploads/1/2016/10/logwebserver.jpg)

The logs can be viewed on web interface:

![Channel Info on logserver](http://rainbowheart.ro/static/uploads/1/2016/10/logserver.jpg)

A sample program client in python:

```python

import logclient
import time

client = logclient.LogClient("localhost","7000")
client.log("Client1 start.","Debug","#FF0000")
time.sleep(1)
client.log("Client1 end.","Debug","#FF0000")


```

Feel free to use this software for both personal and commercial usage.

