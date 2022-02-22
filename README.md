# How expensive is your city?
I built a model to predict how expensive it is to live in any city in the world. The model was built using price indices from hundreds of cities and prices of dozens of items in each city.  

I scraped the data from [expatistan](https://www.expatistan.com/cost-of-living) using BeautifulSoup.  

I used TensorFlow to create a deep neural network (DNN) regression model.  

I used Streamlit to build a web app to showcase the results.

There are three notebooks and two scripts in this proejct.    
1. expatistan_web_scraping.ipynb  
  - notebook for web scraping to gather data
2. linear regression dnn model.ipynb  
  - notebook to build a TensorFlow deep neural network (DNN) regression model
3. linear regression polynomial features.ipynb  
  - notebook to build a linear model using scikit learn
a_scrape_data.py  
  - script for web scraping to gather data  
b_app.py  
  - script for building a Streamlit web app s
