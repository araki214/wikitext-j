#coding: utf-8

import requests
import codecs
import re
import cnvk
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

#漉し取り
def filt(lin,cou):
	jisx0208 = []
	with open("unicode.txt", "r", encoding="utf-8_sig") as f:
		for line in f:
			line = line.strip()
			jisx0208.append(line)
	jisx0208.append('\n')
	jisx0208.append('　')
	jisx0208.append(' ')
	jisx0208.append(' ')
	jisx0208.append('‎')
	jisx0208.append(' ‎')
	Jisx0208 = set(jisx0208)
	h = codecs.open('Exception_F.html', 'a', 'utf-8')
	lin_list = list(lin) 
	for ind,ch in enumerate(lin_list):
		if ch not in Jisx0208:
			print(ch)
			txt = "\n".join(ch)
			Count = str(cou)
			h.write(Count+txt+'\n')
			ch = '*'+ Count+'*'
			cou = cou +1
			lin_list[ind]=ch
	lin = ''.join(lin_list)
	h.close()
	return lin,cou

#リスト作成
def list_sampling(x,y):
	entry = x.get_text('\n')
	if entry not in y:
		y.append(entry)

news_url = "https://ja.wikipedia.org/wiki/秀逸な記事"
html = requests.get(news_url)
soup = BeautifulSoup(html.content, "html.parser")
fo = codecs.open('Featured_List'+ '.txt', 'w', 'utf-8')
list1 = []
for i in soup.select('small'):
	catalog_sample = i.find_next('a')
	list_sampling(catalog_sample,list1)
	catalog_sample_follower = catalog_sample.find_next_siblings('a')
	for j in catalog_sample_follower:
		list_sampling(j,list1)
#余分な'wl'削除＆テキスト書き込み
for line in list1:
	if line.find( 'wl')>-1:
		break				
	else:
		fo.write('\n='+line+'=\n')
fo.close()	


#テキスト抽出(概要)
def sampling(x,y,cou):
	y.append(x)
	leader = x['href']
	list2 = []
	html2 = requests.get('https://ja.wikipedia.org'+leader)
	soup2 = BeautifulSoup(html2.content, "html.parser")
	[s.extract() for s in soup2('sup')]
	#[s.replace_with('削除済') for s in soup2(text =re.compile('#'))]
	title_and_trash = soup2.select('[class~=firstHeading]')
	title = title_and_trash[0].get_text()
	title = cnvk.convert(title,cnvk.Z_ASCII,cnvk.Z_KATA,{u"⋯":u"…"},{u"–":u"―"},{u"—":u"―"},{u"－":u"‐"},{u"－":u"‐"},{u"～":u"〜"},{u"·":u"・"},{u"⋅":u"・"},{u" ":u"　"},{u"›":u"〉"},{u"‹":u"〈"},{u"»":u"》"},{u"«":u"《"},{u"≥":u"≧"},{u"≤":u"≦"},{u"µ":u"μ"},{u"〝":u"“"},{u"〟":u"”"},{u"⁄":u"／"},{u"=":u"＝"})
	title,cou = filt(title,cou)
	fo = codecs.open('Featured_Contents'+ '.txt', 'a', 'utf-8')
	fo.write('\n='+title+'=\n')				
	fo.close()
	starting_point = soup2.select('[class~=toclimit-3],[class~=toc]')
	followers = starting_point[0].find_previous_siblings('p')
	for k in followers:
		follower = k.get_text()
		list2.append(follower)	
		list2.reverse()
	for line in list2:
		line = cnvk.convert(line,cnvk.ZAC,cnvk.ZK,{u"⋯":u"…"},{u"–":u"―"},{u"—":u"―"},{u"－":u"‐"},{u"－":u"‐"},{u"～":u"〜"},{u"·":u"・"},{u"⋅":u"・"},{u" ":u"　"},{u"›":u"〉"},{u"‹":u"〈"},{u"»":u"》"},{u"«":u"《"},{u"≥":u"≧"},{u"≤":u"≦"},{u"µ":u"μ"},{u"〝":u"“"},{u"〟":u"”"},{u"⁄":u"／"},{u"=":u"＝"})
		line,cou = filt(line,cou)
		fo = codecs.open('Featured_Contents'+ '.txt', 'a', 'utf-8')
		fo.write(line)				
		fo.close()
	return cou
		
#テキスト抽出(詳細)
def sampling_detail(x,y,cou):
	y.append(x)
	leader = x['href']
	List = []
	html2 = requests.get('https://ja.wikipedia.org'+leader)
	soup2 = BeautifulSoup(html2.content, "html.parser")
	[s.extract() for s in soup2('sup')]
	[s.extract() for s in soup2('annotation')]
	[s.extract() for s in soup2('.mw-editsection')]
	[s.extract() for s in soup2.select('.gallerybox')]
	[s.extract() for s in soup2.select('.mbox-text')]
	[s.extract() for s in soup2.select('.geo-multi-punct')]
	[s.extract() for s in soup2.select('.geo-nondefault')]
	[s.extract() for s in soup2.select('.geo-default')]
	[s.extract() for s in soup2.select('.plainlist')]	
	block = soup2.select('h2 > span[class~=mw-headline]')
	for i in block:
		over = i.prettify()
		if over.find('id="出典"')>-1 or over.find('id="注釈"')>-1 or over.find('id="脚注"')>-1 or over.find('id="註釈"')>-1 or over.find('id="外部リンク"')>-1:
			break
		item1 = i.get_text()
		item1 = cnvk.convert(item1,cnvk.ZAC,cnvk.ZK,{u"⋯":u"…"},{u"–":u"―"},{u"—":u"―"},{u"－":u"‐"},{u"－":u"‐"},{u"～":u"〜"},{u"·":u"・"},{u"⋅":u"・"},{u" ":u"　"},{u"›":u"〉"},{u"‹":u"〈"},{u"»":u"》"},{u"«":u"《"},{u"≥":u"≧"},{u"≤":u"≦"},{u"µ":u"μ"},{u"〝":u"“"},{u"〟":u"”"},{u"⁄":u"／"},{u"=":u"＝"})
		item1,cou = filt(item1,cou)
		if item1.find('注釈')>-1 or item1.find('脚注')>-1 or item1.find('註釈')>-1:
			break
		List.append('\n=='+item1+'==\n')
		texts = i.find_all_next(['h2','h3','h4','p','li','dd','dt','blockquote'])
		overlap = []
		temp2_prev = texts[0].prettify()
		temp2_tx_prev=''
		for j in texts:
			temp2 = j.prettify()
			if temp2.find('h2')>-1:
				break 
			elif temp2.find('h3')>-1 and temp2.find('mw-headline')>-1:
				heading2 = j.select('.mw-headline')
				item2 = heading2[0].get_text()
				item2 = cnvk.convert(item2,cnvk.ZAC,cnvk.ZK,{u"⋯":u"…"},{u"–":u"―"},{u"—":u"―"},{u"－":u"‐"},{u"－":u"‐"},{u"～":u"〜"},{u"·":u"・"},{u"⋅":u"・"},{u" ":u"　"},{u"›":u"〉"},{u"‹":u"〈"},{u"»":u"》"},{u"«":u"《"},{u"≥":u"≧"},{u"≤":u"≦"},{u"µ":u"μ"},{u"〝":u"“"},{u"〟":u"”"},{u"⁄":u"／"},{u"=":u"＝"})
				item2,cou = filt(item2,cou)
				if item2 not in overlap:
					List.append('\n==='+item2+'===\n')
					overlap.append(item2)
				temp2_prev=temp2
			elif temp2.find('h4')>-1 and temp2.find('mw-headline')>-1:
				heading3 = j.select('.mw-headline')
				item3 = heading3[0].get_text()
				item3 = cnvk.convert(item3,cnvk.ZAC,cnvk.ZK,{u"⋯":u"…"},{u"–":u"―"},{u"—":u"―"},{u"－":u"‐"},{u"－":u"‐"},{u"～":u"〜"},{u"·":u"・"},{u"⋅":u"・"},{u" ":u"　"},{u"›":u"〉"},{u"‹":u"〈"},{u"»":u"》"},{u"«":u"《"},{u"≥":u"≧"},{u"≤":u"≦"},{u"µ":u"μ"},{u"〝":u"“"},{u"〟":u"”"},{u"⁄":u"／"},{u"=":u"＝"})
				item3,cou = filt(item3,cou)
				if temp2_prev.find('h3')==-1 and item3 not in overlap:
					List.append('\n==='+item3+'===\n')
					overlap.append(item3)
				if temp2_prev.find('h3')>-1 and item3 not in overlap:
					List.append('\n===='+item3+'====\n')
					overlap.append(item3)
				temp2_prev=temp2
			elif temp2.find('blockquote')>-1:
				text0 = j.get_text()
				text0 = cnvk.convert(text0,cnvk.ZAC,cnvk.ZK,{u"⋯":u"…"},{u"–":u"―"},{u"—":u"―"},{u"－":u"‐"},{u"－":u"‐"},{u"～":u"〜"},{u"·":u"・"},{u"⋅":u"・"},{u" ":u"　"},{u"›":u"〉"},{u"‹":u"〈"},{u"»":u"》"},{u"«":u"《"},{u"≥":u"≧"},{u"≤":u"≦"},{u"µ":u"μ"},{u"〝":u"“"},{u"〟":u"”"},{u"⁄":u"／"},{u"=":u"＝"})
				text0,cou=filt(text0,cou)
				if text0 not in overlap:
					List.append('<block>'+text0+'<block>\n')
					overlap.append(text0)
				temp2_tx_prev=text0
				temp2_prev=temp2
			elif temp2.find('<dt>')>-1:
				item4 = j.get_text()
				item4 = cnvk.convert(item4,cnvk.ZAC,cnvk.ZK,{u"⋯":u"…"},{u"–":u"―"},{u"—":u"―"},{u"－":u"‐"},{u"－":u"‐"},{u"～":u"〜"},{u"·":u"・"},{u"⋅":u"・"},{u" ":u"　"},{u"›":u"〉"},{u"‹":u"〈"},{u"»":u"》"},{u"«":u"《"},{u"≥":u"≧"},{u"≤":u"≦"},{u"µ":u"μ"},{u"〝":u"“"},{u"〟":u"”"},{u"⁄":u"／"},{u"=":u"＝"})
				item4,cou = filt(item4,cou)
				if temp2_tx_prev.find(item4)==-1:
					if temp2_prev.find('h3')==-1 and item4 not in overlap:
						List.append('\n==='+item4+'===\n')
						overlap.append(item4)
					if temp2_prev.find('h3')>-1 and item4 not in overlap:
						List.append('\n===='+item4+'====\n')
						overlap.append(item4)
					temp2_prev=temp2
			elif temp2.find('<p>')>-1 or temp2.find('<li>')>-1 or temp2.find('<dd>')>-1:
				if temp2.find('mwe-math-element')==-1:
					text = j.get_text()
					text = cnvk.convert(text,cnvk.ZAC,cnvk.ZK,{u"⋯":u"…"},{u"–":u"―"},{u"—":u"―"},{u"－":u"‐"},{u"－":u"‐"},{u"～":u"〜"},{u"·":u"・"},{u"⋅":u"・"},{u" ":u"　"},{u"›":u"〉"},{u"‹":u"〈"},{u"»":u"》"},{u"«":u"《"},{u"≥":u"≧"},{u"≤":u"≦"},{u"µ":u"μ"},{u"〝":u"“"},{u"〟":u"”"},{u"⁄":u"／"},{u"=":u"＝"})
					text,cou=filt(text,cou)
					if temp2_tx_prev.find(text)==-1:
						if text not in overlap:
							List.append(text)
							overlap.append(text)
				elif temp2.find('mwe-math-element')>-1:			
					text = '<math-element>\n'
					if temp2_tx_prev.find(text)==-1:
						List.append(text)
				temp2_prev=temp2
	for line in List:
		fo = codecs.open('Featured_Contents'+ '.txt', 'a', 'utf-8')
		fo.write(line)				
		fo.close()
	return cou	

def main():
	http = []
	count= 1
	for i in soup.select('small'):
		sample = i.find_next('a')
		if sample not in http:
			count=sampling(sample,http,count)
			count=sampling_detail(sample,http,count)
			sample_follower = sample.find_next_siblings('a')
			for n in sample_follower:
				count=sampling(n,http,count)
				count=sampling_detail(n,http,count)
				http.append(n)	
				

if __name__=='__main__':
	main()
