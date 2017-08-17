
from __future__ import division
import urllib2
import re
import lxml.html
from datetime import datetime
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import string
import nltk, re, pprint
from nltk import word_tokenize

##################################################################################

def download(url, user_agent='liter', num_retries=2):
    # downloads page HTML from the given url
    
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                #recursively retry 5xx HTTP errors
                return download(url, user_agent, num_retries-1)   
    return html

##################################################################################

def genre_urls_dic(genre_url):
    # given a genre, and a seed url, output a dictionary of all stats/stories/urls for a given genre
    
    genre = re.findall('^.+/c/(.+)|$',genre_url)[0]
    url = genre_url+'/1-page'
    html = download(url)
    tree = lxml.html.fromstring(html)
    pages = int(tree.xpath('//div[@class="b-pager-pages"]/form/select/option/text()')[-1])
    
    genre_data = []
    
    for i in range(1,pages+1):
        page_url = genre_url+'/%s-page' % (i)
        # harvest data
        ## get each div element containing a story
        story_roots = tree.xpath('//div[@class="b-sl-item-r w-34t"]')
        ## loop through story div elements to get associated data, append data as a dic
        for root in story_roots:
            story_data = {}
            story_data['genre'] = genre
            story_data['url'] = root.xpath('./h3/a/@href')[0]
            story_data['story_id'] = re.findall('^.+/s/(.+)|$', story_data['url'])[0]
            story_data['title'] = root.xpath('./h3/a/text()')[0]
            story_data['desc'] = re.sub(u'\xa0\u2014\xa0','',root.xpath('./span[@class="b-sli-description p-57u"]/text()')[0])
            story_data['author_name'] = root.xpath('./span[@class="b-sli-meta"]/span[@class="b-sli-author"]/a/text()')[0]
            story_data['author_id'] = re.findall('.*uid=(\w+)&|$',root.xpath('./span[@class="b-sli-meta"]/span[@class="b-sli-author"]/a/@href')[0])[0]
            story_data['created_date'] = datetime.strptime(root.xpath('./span[@class="b-sli-meta"]/span[@class="b-sli-date"]/text()')[0], '%m/%d/%y')
            try:
                story_data['rating'] = float(root.xpath('./span[@class="b-sli-meta"]/span[@class="b-sli-rating"]/text()')[0])
            except (IndexError, ValueError):
                story_data['rating'] = None
            
            genre_data.append(story_data)
         
    return genre_data

##################################################################################

def get_story(story_url):
    # given a story url, downloads the body of the story and associated data
    
    html = download(story_url)
    tree = lxml.html.fromstring(html)
    pages = int(re.findall('\d+',tree.xpath('//div[@class="b-pager-pages"]/span[@class="b-pager-caption-t r-d45"]/text()')[0])[0])
    text = tree.xpath('//div[@class="b-story-body-x x-r15"]/div/p/text()')
    stats = tree.xpath('//div[@class="b-story-stats-block"]/span[@class="b-story-stats"]/text()')
    comments = int(re.findall('\d+',stats[0])[0])
    views = int(re.findall('\d+',stats[1])[0])
    favorites = int(re.findall('\d+',stats[2])[0])
    tags = tree.xpath('//div[@class="b-s-story-tag-list"]/ul/li/a/text()')
    
    # creates a list of the first page of text. Output of initial scrape is a list 
    story_text = []
    story_text += text    
    
    # if there is more than one page to the story, 
    if pages > 1:
        for i in range(1,pages):
            page_url = story_url + '?page=%s' % (i+1)
            page_html = download(page_url)
            page_tree = lxml.html.fromstring(page_html)
            page_text = page_tree.xpath('//div[@class="b-story-body-x x-r15"]/div/p/text()')
            story_text += page_text
            if i == pages-1:
                tags = page_tree.xpath('//div[@class="b-s-story-tag-list"]/ul/li/a/text()')
    
    # output dict of collected data for database
    story_data = {
        'pages':pages,
        'comments':comments,
        'views':views,
        'favorites':favorites,
        'tags':tags,
        'story_text':" ".join(story_text),
        }
    
    return story_data



















