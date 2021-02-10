# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     fetchScheduler
   Description :
   Author :        JHao
   date：          2019/8/6
-------------------------------------------------
   Change Activity:
                   2019/08/06:
-------------------------------------------------
试图改为多线程
"""
__author__ = 'JHao'

from threading import Thread
from handler.logHandler import LogHandler
from handler.proxyHandler import ProxyHandler
from fetcher.proxyFetcher import ProxyFetcher
from handler.configHandler import ConfigHandler


class Fetcher(Thread):
    name = "fetcher"

    def __init__(self, set, logger, fetch_name):
        Thread.__init__(self,name=fetch_name)
        self.name = fetch_name
        self.log = logger
        self.proxy_set = set
        self.conf = ConfigHandler()
        self.proxy_handler = ProxyHandler()

    def run(self):
        self.log.info("ProxyFetch - {func}: start".format(func=self.name))
        fetcher = getattr(ProxyFetcher, self.name, None)
        if not fetcher:
            self.log.error("ProxyFetch - {func}: class method not exists!")
        if not callable(fetcher):
            self.log.error("ProxyFetch - {func}: must be class method")

        try:
            for proxy in fetcher():
                if proxy in self.proxy_set:
                    self.log.info('ProxyFetch - %s: %s exist' % (self.name, proxy.ljust(23)))
                    continue
                else:
                    self.log.info('ProxyFetch - %s: %s success' % (self.name, proxy.ljust(23)))
                if proxy.strip():
                    self.proxy_set.add(proxy)
        except Exception as e:
            self.log.error("ProxyFetch - {func}: error".format(func=self.name))
            self.log.error(str(e))


def runFetcher():
    thread_list = list()
    proxy_set = set()
    log = LogHandler('fetcher')
    fetch_names = ConfigHandler().fetchers
    
    for fetch_name in fetch_names:
        thread_list.append(Fetcher(proxy_set, log, fetch_name))

    log.info("ProxyFetch : start")
    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    log.info("ProxyFetch - all complete!")
    return proxy_set
