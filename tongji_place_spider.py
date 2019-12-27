import requests
from lxml import etree
import time
import json

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36,',
	# 'Host': 'www.stats.gov.cn',
	# 'Cookie': '_trs_uv=k163tn1b_6_51kd; AD_RS_COOKIE=20080918',
}

start_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'
time.sleep(3)
rep = requests.get(start_url, headers=headers)
rep.encoding = rep.apparent_encoding
Text = rep.text
sel = etree.HTML(Text)

Province_names = sel.xpath('//*[@class="provincetr"]/td/a/text()')   # 省或直辖市名称
Province_urls = sel.xpath('//*[@class="provincetr"]/td/a/@href')     # 省或直辖市url

China_place_data = {}
china_place_data = {}

for Province_name, Province_url in zip(Province_names, Province_urls):

	Province_url = start_url + Province_url
	rep = requests.get(Province_url, headers=headers)
	time.sleep(3)
	rep.encoding = rep.apparent_encoding
	sel = etree.HTML(rep.text)

	Province = []     # 省份下地名列表

	City_names = sel.xpath('//tr[@class="citytr"]/td[2]/a/text()')  # 地级市名称
	City_urls = sel.xpath('//tr[@class="citytr"]/td[2]/a/@href')    # 地级市url

	Province += City_names  # 加入省份下地名列表
	china_place_data[Province_name] = {}


	for City_name, City_url in zip(City_names, City_urls):

		City_url = start_url + City_url
		rep = requests.get(City_url, headers=headers)
		time.sleep(3)
		rep.encoding = rep.apparent_encoding
		sel = etree.HTML(rep.text)

		County_names = sel.xpath('//tr[@class="countytr"]/td[2]/a/text()')   # 区名称
		County_urls = sel.xpath('//tr[@class="countytr"]/td[2]/a/@href')    # 区url

		Province += County_names  # 加入省份下地名列表
		china_place_data[Province_name][City_name] = {}

		for County_name, County_url in zip(County_names, County_urls):

			County_url = Province_url.replace('.html', '/') + County_url
			rep = requests.get(County_url, headers=headers)
			time.sleep(3)
			rep.encoding = rep.apparent_encoding
			Text = rep.text
			sel = etree.HTML(Text)

			Town_names = sel.xpath('//tr[@class="towntr"]/td[2]/a/text()')   # 镇名称
			Town_urls = sel.xpath('//tr[@class="towntr"]/td[2]/a/@href')     # 镇url

			Province += Town_names  # 加入省份下地名列表

			china_place_data[Province_name][City_name][County_name] = Town_names
			print('{}采集完毕'.format(County_name))

	print('{}采集完毕'.format(Province_name))

	China_place_data[Province_name] = Province

print(China_place_data)
print(china_place_data)

China_place_data = json.dumps(China_place_data)    # 转换为json格式
china_place_data = json.dumps(china_place_data)    # 转换为json格式

with open('China_place_data.json', 'w') as f:   # 保存为json文件
	f.write(China_place_data)

with open('china_place_data.json', 'w') as f:   # 保存为json文件
	f.write(china_place_data)











