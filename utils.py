from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
def get_headers():
    ua = UserAgent()
    return ua.random

def get_text(url):
    headers = {'User-Agent': get_headers()}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # 确保正确的编码
    return response

def get_subtxt(url):
    url = 'https://www.notion.so'+url
    response = get_text(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find_all('article',class_="helpArticle_helpArticle__devPW")
    return_arr = []
    if not article:#还存在子链接继续嵌入
        article_subs = soup.find_all('article', class_="help-center-guides-grid-item")
        for sub in article_subs:
            title3 = sub.find('h2').text
            print(f"[子链接多层嵌入] || {title3} 抓取中...")
            href = sub.find('a')['href']
            response = get_text('https://www.notion.so'+href)
            soup = BeautifulSoup(response.text, 'html.parser')
            sections = soup.find_all('div',class_="contentfulRichText_bodyLimit__F5GOU")
            sub_content = []
            for section in sections:
                content = section.text.strip()
                if content:  # 结果不为空再返回
                    sub_content.append(content)
            return_arr.append({title3:sub_content})
            print(f"[子链接多层嵌入] || {title3} 抓取完毕...")
    else:
        article = article[0]
        sections = article.find_all('section')
        for section in sections:
            content = section.text.strip()
            if content: #结果不为空再返回
                return_arr.append(content)
    # print(return_arr)
    return return_arr



if __name__=="__main__":
    content = get_subtxt('/help/guides/category/documentation')
    print(content)