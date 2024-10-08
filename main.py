from bs4 import BeautifulSoup
from utils import get_text,get_subtxt
import json

def main(url):
    """部分章节存在子链接多层嵌入：在get_subtxt中处理完毕"""
    response = get_text(url)
    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')
    #获取大标题
    title = soup.find_all('span',class_="text_text__cG3pf text_textWeightBold__NuyUS text_textSizeCaption__3Geg0")[0].text
    output_dic = {title:[]} #结果文档
    # 获取章节
    dls = soup.find_all('dl',class_="toggleList_toggleList__X4yHc")  # 假设文档标题在<h2>标签中
    for dl in dls:
        dt = dl.find('dt').text #章节一级标题
        print(f"{dt} 抓取中...")
        tem_ss = {dt:[]} #每一章存一个字典
        dds = dl.find_all('dd')
        for dd in dds:
            a = dd.find('a')
            title2 = a.text #章节二级标题
            href = a['href']
            content = get_subtxt(href) #子链接内容
            tem_ss[dt].append({title2:content})#每一小章存一个小字典
        output_dic[title].append(tem_ss)
        print(f"{dt} 抓取完毕...")

    with open('output.json', 'w') as json_file:
        json.dump(output_dic, json_file, indent=2)
if __name__=="__main__":
    # 目标URL
    url = 'http://www.notion.so/help'
    main(url)