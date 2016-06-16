# -*- coding: utf-8 -*-
# python 2.7
import urllib2, socket, socks

class Tor:
    def __init__(self):
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
        socket.socket = socks.socksocket
    def test(self):
        return urllib2.urlopen("https://api.ipify.org?format=json").read()

if __name__ == "__main__":
    Tor = Tor()
    ip = Tor.test()
    print ip # Torを経由したIPアドレスが表示される。