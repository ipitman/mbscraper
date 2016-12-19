
from lxml import html
import requests

def get_tree(link):
	return html.fromstring(requests.get(link).content)

def make_dict():
	product_dict = {}
	tree = get_tree('http://www.performancebike.com/webapp/wcs/stores/servlet/CategoryDisplay?storeId=10052&catalogId=10551&langId=-1&orderBy=&searchTerm=&beginIndex=0&pageSize=1000&parent_category_rn=400001&top_category=400001&categoryId=400308&metaData=')
	products = tree.xpath('/html/body/div[@id="mainPage"]/div[@id="pb-content-area"]/div[@id="pb-content-column"]/div[@id="pb-product-grid"]/ul/li[@class="product"]/div[@class="product-info"]/h2/a/@href')
	for link in products:
		subtree = get_tree("http://www.performancebike.com/webapp/wcs/stores/servlet/" + link)
		spec_types = subtree.xpath('/html/body/div[@id="mainPage"]/div[@class="productdetailpage"]/div[@class="media_addtocart_container"]/div[@class="product_media_container"]/div[@class="productinfo_recommended_container"]/div[@class="productinfo_review_container"]/div[@id="tabcontent_container"]/div[@id="specsDiv"]/dl/dt/text()')
		specs = subtree.xpath('/html/body/div[@id="mainPage"]/div[@class="productdetailpage"]/div[@class="media_addtocart_container"]/div[@class="product_media_container"]/div[@class="productinfo_recommended_container"]/div[@class="productinfo_review_container"]/div[@id="tabcontent_container"]/div[@id="specsDiv"]/dl/dd/text()')
		name = subtree.xpath('/html/body/div[@id="mainPage"]/div[@class="productdetailpage"]/div[@class="media_addtocart_container"]/div[@class="add_to_cart_container"]/form[@id="OrderItemAddForm"]/h1[@class="product_title"]/text()')[0].strip('\r\n\t ')
		msrp = subtree.xpath('/html/body/div[@id="mainPage"]/div[@class="productdetailpage"]/div[@class="media_addtocart_container"]/div[@class="add_to_cart_container"]/form[@id="OrderItemAddForm"]/div[@class="price_reviews_container"]/div[@class="price_compare"]/dl[@class="sr_product_price_display product_page"]/dd[@class="sr_product_price"]/span[@class="msrp_price_val has_sale_price"]/text()')
		if msrp:
			sale_price = subtree.xpath('/html/body/div[@id="mainPage"]/div[@class="productdetailpage"]/div[@class="media_addtocart_container"]/div[@class="add_to_cart_container"]/form[@id="OrderItemAddForm"]/div[@class="price_reviews_container"]/div[@class="price_compare"]/dl[@class="sr_product_price_display product_page"]/dd[@class="sr_product_price"]/span[@class="sale_price_val"]/text()')
		else:
			msrp = subtree.xpath('/html/body/div[@id="mainPage"]/div[@class="productdetailpage"]/div[@class="media_addtocart_container"]/div[@class="add_to_cart_container"]/form[@id="OrderItemAddForm"]/div[@class="price_reviews_container"]/div[@class="price_compare"]/dl[@class="sr_product_price_display product_page"]/dd[@class="sr_product_price"]/span[@class="msrp_price_val"]/text()')
			sale_price = subtree.xpath('/html/body/div[@id="mainPage"]/div[@class="productdetailpage"]/div[@class="media_addtocart_container"]/div[@class="add_to_cart_container"]/form[@id="OrderItemAddForm"]/div[@class="price_reviews_container"]/div[@class="price_compare"]/dl[@class="sr_product_price_display product_page"]/dd[@class="sr_product_price"]/span[@class="list_price_val"]/text()')
		subdict = dict(zip(spec_types, specs))
		subdict['msrp:'] = float(msrp[0].replace('$','').replace(',',''))
		subdict['sale price:'] = float(sale_price[0].replace('$','').replace(',',''))
		product_dict[name] = subdict
	return product_dict

def valid_spec_types(bike_dict):
	valid_list = []
	for bike in bike_dict:
		for key in bike_dict[bike]:
			if (key not in valid_list) and (key != 'msrp:') and (key != 'sale price:'):
				valid_list.append(key)
	return valid_list

def spec_filter(bike_dict, spec_type, spec):
	new_bike_dict = {}
	for bike in bike_dict:
		if spec_type in bike_dict[bike]:
			if spec in bike_dict[bike][spec_type]:
				new_bike_dict[bike] = bike_dict[bike]
	return new_bike_dict

def price_filter(bike_dict, lb=0, ub=float('inf')):
	new_bike_dict = {}
	for bike in bike_dict:
		if lb <= bike_dict[bike]['sale price:'] <= ub:
			new_bike_dict[bike] = bike_dict[bike]
	return new_bike_dict

def cheapest_bike(bike_dict):
	return min(bike_dict.items(), key=lambda x: x[1]['sale price:'])




