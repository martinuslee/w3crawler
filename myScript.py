from urllib.request import urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup
import csv
import time
import googletrans 

tagList = ['html','head', 'body', 'title', 'meta', 'div', 'a', 'script', 'link', 'img',
            'span','p', 'li', 'ul',  'style', 'br','hn',
           'input', 'form', 'nav', 'footer', 'header', 'iframe', 'button', 'strong', 'i']


def html_tag_crawling(input):
    outList = []
    translator = googletrans.Translator()
    for tag in input:
        try:
            html = urlopen(
                'https://www.w3schools.com/tags/tag_' + tag + '.asp')
            bs = BeautifulSoup(html, 'html.parser')

            nameList = bs.findAll({'p', 'h2'})
            txtList = []
            for i in range(len(nameList)):
                txtList.append(nameList[i].get_text())

            txtList = txtList[txtList.index(
                'Definition and Usage')+1:txtList.index('Browser Support')-1]
            txtList = [word.replace("\n", "") for word in txtList]
            txtList = ' '.join(txtList)
            result = translator.translate(txtList, dest='ko')
            outList.append(result.text)
            # print(txtList)
        except HTTPError as e:
            print(e)
    return outList


if __name__ == "__main__":
    start = time.time()
    output = html_tag_crawling(tagList)
    # print(output)
    with open('tagList.csv', 'w') as f:
        writer = csv.writer(f)
        for val in output:
            writer.writerow([val])

    print('finish ', round(time.time() - start, 2), 'seconds')
