import urllib2
import re
import lxml.html


def download(url, file, user_agent='liter', num_retries=2):
    print('Downloading', url)
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        f = open(file,'w')
        html = urllib2.urlopen(request).read()
        f.write(html)
        f.close()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                #recursively retry 5xx HTTP errors
                return download(url, file, user_agent, num_retries-1)
    
    msg = "Wrote HTML %s to %s" % (html[:15],file)
    
    return msg
        
def get_fields(html):
    tree = lxml.html.fromstring(html)
    title = tree.xpath('//title/text()')[0]
    pages = re.match('\d+',tree.xpath('//span[@class="b-pager-caption-t r-d45"]/text()')[0]).group()
    body = ''.join(tree.xpath('//div[@class="b-story-body-x x-r15"]/div/p/text()'))
    