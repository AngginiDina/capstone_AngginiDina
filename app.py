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

table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr') #tbody apakah perlu ganti jadi -table --> tr = table.find_all('tr')
temp = [] #initiating a tuple

for i in range(1, len(tr)):
    #insert the scrapping process here
    row = table.find_all('tr')[i]

    #get tanggal
    tgl = row.find_all('td')[0].text
    tgl = tgl.strip() #for removing the excess whitespace
    
    #get harga harian
    hargaharian = row.find_all('td')[2].text
    hargaharian = hargaharian.strip() #for removing the excess whitespace
    
    
    temp.append((tgl,hargaharian)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('tgl', 'hargaharian'))

#insert data wrangling here
df['hargaharian'] = df['hargaharian'].str.replace("IDR","")
df['hargaharian'] = df['hargaharian'].str.replace(",","").astype('float64')
df['tgl'] = df['tgl'].astype('datetime64')
df = df.set_index('tgl')


#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {df["hargaharian"].mean()}'

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
