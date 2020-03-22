#!/usr/bin/env python
# coding: utf-8

# In[38]:


# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


def scrape_all():
   # Initiate headless driver for deployment
   # Mac users
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	browser = Browser("chrome", executable_path="chromedriver", headless=True)

	#set our news title and paragraph variables
	news_title, news_paragraph = mars_news(browser)

	# Run all scraping functions and store results in dictionary
	data = {
    	"news_title": news_title,
    	"news_paragraph": news_paragraph,
    	"featured_image": featured_image(browser),
    	"facts": mars_facts(),
    	"last_modified": dt.datetime.now()
}


# In[25]:

def mars_news(browser):

	# Visit the mars nasa news site
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)
	# Optional delay for loading the page
	browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


	# In[26]:


	html = browser.html
	news_soup = BeautifulSoup(html, 'html.parser')
	slide_elem = news_soup.select_one('ul.item_list li.slide')


	# In[27]:

	# Add try/except for error handling
    try:
		slide_elem.find("div", class_='content_title')


		# In[28]:


		# Use the parent element to find the first `a` tag and save it as `news_title`
		news_title = slide_elem.find("div", class_='content_title').get_text()


		# In[29]:


		news_title


		# In[30]:


		# Use the parent element to find the paragraph text
		news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

	except AttributeError:
        return None, None
		
	return news_title, news_p


# ### Featured Images

# In[31]:

def featured_image(browser):

# Visit URL
	url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(url)


	# In[32]:


	# Find and click the full image button
	full_image_elem = browser.find_by_id('full_image')
	full_image_elem.click()


	# In[33]:


	# Find the more info button and click that
	browser.is_element_present_by_text('more info', wait_time=1)
	more_info_elem = browser.links.find_by_partial_text('more info')
	more_info_elem.click()


	# In[35]:


	# Parse the resulting html with soup
	html = browser.html
	img_soup = BeautifulSoup(html, 'html.parser')


	# In[36]:

	try:
	# Find the relative image url
		img_url_rel = img_soup.select_one('figure.lede a img').get("src")

	except AttributeError:
		return None

	return img_url

	# In[37]:


	# Use the base URL to create an absolute URL
	img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
	img_url


# In[39]:

def mars_facts():
	try:
		df = pd.read_html('http://space-facts.com/mars/')[0]
	except BaseException:
        return None

	df.columns=['description', 'value']
	df.set_index('description', inplace=True)
	# Convert dataframe into HTML format, add bootstrap
    return df.to_html()



# In[41]:


	browser.quit()


# In[ ]:

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


