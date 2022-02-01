#from niconico_dl import NicoNico
import niconico_dl
import requests, bs4
import sys
import pprint
from pathlib import Path

import tkinter
import tkinter.ttk as ttk



def download():
    #mylist_url = 'https://www.nicovideo.jp/user/21514289/mylist/61271803'
    mylist_url = url_.get()
    if 'https' not in mylist_url:
        return

    res = requests.get(mylist_url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    print('soup')
    pprint.pprint(soup)


    elems = soup.select('li', class_='WktkEnvironment')
    elems = soup.find_all('script')

    #elems = soup

    print('elems')
    pprint.pprint(elems)
    for elem in elems:
        url =  elem.get('id')
        print('elem')
        print(elem)
        
    elem = elems[-1]
    text_list = str(elem).split("\"")
    urls = []
    for url in text_list:
        if url.startswith("http") and 'watch' in url and 'autoplay' not in url:
            urls.append(url)
            print(url)


    urls = list(set(urls))
    print(urls)

    import time
    for url in urls:
        sm_n  = url.split('sm')[-1]
        #url = "https://www.nicovideo.jp/watch/sm35088071"
        u = f"https://www.nicovideo.jp/watch/sm{sm_n}"
        with niconico_dl.NicoNicoVideo(u, log=True) as nico:
            data = nico.get_info()
            nico.download(data["video"]["title"] + ".mp4")

        time.sleep(30)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('niconico mylist downloader')
    root.geometry("300x50")
    url_ = tkinter.StringVar()
    url_entry  = ttk.Entry(root,
                            textvariable=url_,
                            width=90)

    url_entry.grid()
    url_entry.set()
    button = tkinter.Button(root, text="download", command=download)
    button.grid()
    
    root.mainloop()