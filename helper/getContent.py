from bs4 import BeautifulSoup
import requests
import re
import pprint

SOURCE = 'https://story.beva.com'

STYLES = {'睡前故事', '启蒙故事', '亲子故事', '格林童话', '成语故事',
          '安徒生童话', '名人故事', '伊索寓言', '神话故事'}

def func(bf, title):
    content_block = bf.find_all('div', id='stcontent')
    if len(content_block) == 0: return None

    style_block = bf.find_all('p', class_='stcatvc')
    tr_style = r'title="(.*?)">'
    try:
        style = re.findall(tr_style, str(style_block[0]))
        style = style[0]
    except:
        return None

    if style not in STYLES: return None

    tr_content = r'<p>(.*?)</p>'
    paragraphs = re.findall(tr_content, str(content_block[0]))
    content = '\n'.join(paragraphs)
    return dict(title = title, style = style, content = content)