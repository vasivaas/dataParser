import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
	r = requests.get(url)
	return r.text


def write_csv(data):
	with open('stat.csv', 'a') as f:
		writer = csv.writer(f)
		writer.writerow((data['item_name'],
						 data['game_name'],
						 data['price']))
	

def get_page_data(html): #, list_name=[]
	soup = BeautifulSoup(html, 'lxml')
	
	ads = soup.find('div', id="searchResultsRows").find_all('a', class_="market_listing_row_link")
	
	for ad in ads:
		try:
			name = ad.find('div', class_="market_listing_searchresult").get("data-hash-name") #.find('div', class_="market_listing_item_name_block").find('span', class_="market_listing_item_name").text
		except:
			name = ''
		try:
			game_name = ad.find('div', class_="market_listing_searchresult").find('div', class_="market_listing_item_name_block").find('span', class_="market_listing_game_name").text
		except:
			game_name = ''
		try:		
			price = ad.find('div', class_="market_listing_searchresult").find('div', class_="market_listing_price_listings_block").find('div', class_="market_listing_their_price").find('span', class_="normal_price").text.strip()
		except:
			price = ''
		#list_name.append([name, game_name, price])
		data = {
			'item_name': name,
			'game_name': game_name,
			'price': price
		}
		write_csv(data)

def main():
	base_url = 'https://steamcommunity.com/market/search?'
	query_part = '_popular_desc'
	
	
	page_part = input("Enter URL: ")
	
	
	first_page = int(input("Enter the START PAGE: "))
	end_page = int(input("Enter the END PAGE: "))
	#list_name = []
	for p in range(first_page, end_page + 1):
		url_gen = base_url + page_part + str(p) + query_part
		#print(url_gen)
		html = get_html(url_gen)
		get_page_data(html) #, list_name	

		
if __name__ == '__main__':
	main()