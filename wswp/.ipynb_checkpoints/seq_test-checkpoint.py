# -*- coding: utf-8 -*-

from wswp_crawler import link_crawler
from mongo_cache import MongoCache
from alexa_cb import AlexaCallback


def main():
    scrape_callback = AlexaCallback()
    cache = MongoCache()
    #cache.clear()
    link_crawler(seed_url=scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache)


if __name__ == '__main__':
    main()
