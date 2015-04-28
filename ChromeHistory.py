import sqlite3
import os
import sys
import numpy as np
from urlparse import urlparse
from matplotlib import pyplot as plt


for path in (
        os.path.expanduser('~/.config/google-chrome/'),
        os.path.expanduser('~/.config/chromium/'),
        'C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\'
        % os.environ.get('USERNAME'),
        'C:\\Documents and Settings\\%s\\Local Settings\\ \
        Application Data\\Google\\Chrome\\' % os.environ.get('USERNAME')
        ):
    path += os.path.join('Default', 'History')
    if os.path.exists(path):
        break
else:
    print 'Chrome history file not found!'
    sys.exit()
 
conn = sqlite3.connect(path)
c = conn.cursor()
 
c.execute("SELECT urls.url, urls.visit_count, \
          datetime(visits.visit_time/1000000-11644473600, \
          'unixepoch','localtime') \
          FROM urls, visits WHERE urls.id = visits.url")

results = c.fetchall()

history = {}

for result in results:
    site = urlparse(result[0]).netloc
    count = result[1]
    lastVisited = result[2]
    if site in history:
        history[site] += 1    
    else:
        history[site] = 1

toPlot = {}


""" Sort and iterate over the 30 most visited sites only """
for site in sorted(history, key=history.get, reverse=True)[:30]:
    print site, history[site]
    toPlot[site] = history[site]

visits = [toPlot[site] for site in toPlot]
ypos = np.arange(len(visits))
plt.barh(ypos, visits, align='center')
plt.yticks(ypos, [x for x in toPlot])
plt.show()
    

