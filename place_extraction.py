import jieba
import re
import json

Procince_data = open('./China_place_data.json', encoding="utf-8").read()   # 加载地名数据
Procince_data = json.loads(Procince_data)

Procince_Data = {}
for i in Procince_data:
    Procince_Data[i] = re.findall("'(.*?)'", str(Procince_data[i]))  # 整理成每个{省份1:[地名1, 地名2, ....], 省份2:[...]} 形式

def extract_Prefecture_level_city(words, Provincial_data, Provincial_name):
    """
    根据输入公司名 提取出公司所属地级市
    :param words: 公司名
    :param Provincial_data: 公司所属省份的地名数据
    :param Provincial_name: 公司所属省份
    :return:
    """
    words = jieba.lcut(words)
    ls = ["高新", "高新区", "文化", "国有", "资产", "国有资产", "城市", "国有资本"]
    City_ls = ['天津', '上海', '北京', '重庆']   # 直辖市列表
    Words = [i.replace('省', '').replace('市', '') for i in words[0: 2] if i not in ls]  # 只保留前两个个词
    Territory = ''
    city_ls = [city for city in Provincial_data]  # 所在省份地级市列表
    Provincial_name = Provincial_name.replace('省', '').replace('市', '').replace('自治区', "")
    for i in range(len(Words)):
        word = Words[i]
        if i == 0:  # 对第一个词的匹配
            if word == Provincial_name or word in Provincial_name or Provincial_name in word:  # 第一个词为直辖市，自治区或省 修改Territory为省本级或市辖区
                for C_name in City_ls:
                    if C_name in word or C_name == word or word in C_name:  # 提取出的地名 是直辖市 修改 Territory为市辖区
                        Territory = '市辖区'
                else:
                    Territory = '省本级'
                if len(Words) == 1:   # 若只提取出一个词 返回
                    return Territory
                continue
            else:      # 提取出的地名 非直辖市，自治区或省名称
                for City in city_ls:
                    if word == City or word in City or City in word:   # 若等于地级市名称 返回地级市名称

                        return City
                for city in Provincial_data:   # 循环查找每个地级市对应的地名列表 若匹配成功 返回地级市名称
                    for i in Provincial_data[city]:
                        if word in i or word == i:
                            return city
        else:  # 对第二个词进行匹配
            for city in Provincial_data:  # 循环查找每个地级市对应的地名列表 若匹配成功 返回地级市名称
                for i in Provincial_data[city]:
                    if word in i or word == i:
                        return city
            if Territory == '省本级' or Territory == "市辖区":  # 若查找失败 且第一个词的Territory为省本级 或 市辖区 直接返回
                return Territory
            return '暂无'  # 全部查找失败，返回暂无


def extract_province(Procince_Data, company_name):
    """
    根据带地区的公司名称提取所属省份
    :param Procince_Data: 
    :param company_name: 
    :return: 
    """
    flag = re.findall(r'[a-z]+', company_name)
    if flag != []:
        return '暂无'
    ls = ["高新", "高新区", "文化", "国有", "资产", "国有资产", "城市"]
    try:
        words = jieba.lcut(company_name)
        Word = [i.replace('省', '').replace('市', '') for i in words[0: 2] if i not in ls][0]  # 只保留前两个个词
        for province in Procince_Data:
           for place in Procince_Data[province]:
              if "街道" not in place and "基地" not in place and "办事处" not in place:
                  if Word in place or Word == place:
                      return province
        return '暂无'
    except Exception as e:
        return '暂无'