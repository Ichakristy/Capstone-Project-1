from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('div', attrs={'class':'table-responsive'})
tr = table.find_all('tr')
temp = [] #initiating a tuple

for i in range(1, len(tr)):
#insert the scrapping process here
    tr = table.find_all('tr')[i]
    
    #get tanggal
    Date = tr.find_all('td')[0].text
    Date = Date.strip() #for removing the excess whitespace
      
    #get Hari
    Day = tr.find_all('td')[1].text
    Day = Day.strip() #for removing the excess whitespace
    
    #get Rate
    Rate = tr.find_all('td')[2].text
    Rate = Rate.strip() #for removing the excess whitespace
    
    temp.append((Date, Day, Rate)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame (temp, columns = ('Date', 'Day','USD-IDR Rate'))

#insert data wrangling here
df['Date']= pd.to_datetime(df['Date'])
df['Day'] = df['Day'].astype('category')
df['USD-IDR Rate'] = df['USD-IDR Rate'].str.replace("IDR","")
df['USD-IDR Rate'] = df['USD-IDR Rate'].str.replace(",","")
df['USD-IDR Rate'] = df['USD-IDR Rate'].astype('float')

df = df.set_index('Date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {df["USD-IDR Rate"].mean()}'

	# generate plot
	ax = df.plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
