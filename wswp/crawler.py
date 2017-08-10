import wswp_crawler

wswp_crawler.link_crawler('http://example.webscraping.com/', '/(index|view)', max_depth=-1, scrape_callback=wswp_crawler.ScrapeCallback())