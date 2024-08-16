from flask import Flask, request, render_template
#import pandas as pd
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    location = request.form['location']
    
    url = f"https://www.yellowpages.com/search?search_terms={query}&geo_location_terms={location}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    businesses = []
    for listing in soup.find_all('div', class_='result'):
        name = listing.find('a', class_='business-name').text.strip()
        phone = listing.find('div', class_='phones').text.strip()
        address = listing.find('div', class_='street-address').text.strip()
        businesses.append({'name': name, 'phone': phone, 'address': address})
    
    return render_template('results.html', businesses=businesses)

if __name__ == '__main__':
    app.run(debug=True)