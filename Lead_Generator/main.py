from flask import Flask, request, render_template
import pandas as pd
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    business_type = request.form['business_type']
    business_state  = request.form['business_state']
    business_city = request.form['business_city']
    
    url = f'https://www.yellowpages.com/search?search_terms={business_type}&geo_location_terms={business_city}%2C+{business_state}'
    page = requests.get(url)
    yp_soup = BeautifulSoup(page.text, 'html.parser')
    
    companies = yp_soup.find_all(class_='result')

    yp_business_names = []
    yp_phones = []
    yp_address_list = []

    for company in yp_soup.find_all('div',class_='result'):
        name = company.find('a',class_='business-name')
        b_name = name.text.strip() if name else 'None'
        #print(b_name)
        phone = company.find('div',class_='phones phone primary')
        phone_num = phone.text.strip() if phone else 'None'
        #print(phone_num)
        address = company.find('div',class_='street-address')
        street_address = address.text.strip() if address else 'None'
        #print(street_address)
        yp_business_names.append(b_name)
        yp_phones.append(phone_num)
        yp_address_list.append(street_address)
    
    df = pd.DataFrame({
        'Company Name': yp_business_names,
        'Phone Number': yp_phones,
        'Address': yp_address_list,
    })
    df = df.sort_values(by='Company Name')
    df_html = df.to_html(classes='table table-striped', index=False)

    return render_template('results.html', table=df_html)

if __name__ == '__main__':
    app.run(debug=True)
