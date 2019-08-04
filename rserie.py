#!/usr/bin/env python3
import sys
from bs4 import BeautifulSoup as bs
import argparse
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import colorama
from colorama import Fore, Style, Back
import re
colorama.init()



class Page(QWebEnginePage):
    ''' automates the engine '''

    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()

def get_quick_calendar(soup,name):
    ''' get a quick snapshot of the date and the episode aired '''
    data = {}
    episode = []
    name_series = soup.find_all("tr")
    serie_content = [row for row in name_series if name in str(row)]

    for row in serie_content:
        tds = row.find_all("td")
        tde = row.find_all("small")

        for i in range(2,7):
            episode.append(tde[i].text if tds[i].text else '')

    s = soup.title.string
    ep = s[s.find('')].strip()

    data[ep] = episode

    print(Fore.RED +"\n\n\n\nINFO :" + Fore.CYAN + Style.BRIGHT + " {} : {} : ".format(name, data[ep]), end=" ")

def get_quick_info_serie(soup, name):
    ''' get the date of the last episode and the next aired'''
    url_fiche_serie = "https://www.subfactory.fr/series.html&action=g_serie&serieID="

    def ID():
        ''' last part of the url '''
        serieId = soup.find_all("a")
        for i in serieId:
            ret = i.get("href")
            rett = i.get_text()
            if rett == str(a):
                return ret[-4:]
    url = url_fiche_serie + ID()
    page = Page(url)
    p = bs(page.html, "html.parser")

    i = p.find(id="nextSeasonInfo_{}".format(ID()))
    print(Fore.RED + "\n\n\n\nINFO :" + Fore.CYAN +
          Style.BRIGHT + Fore.RED + "\n\n\n\n\n\t\t\t\t"+ name + Fore.CYAN + "\n\n\n\n" + i.text)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="add - for multiple names")
    parser.add_argument("-pv",action='store_true', help="get the previous and the next episode" )
    parser.add_argument("-c",action='store_true', help="get the previous and the next episode" )

    args = parser.parse_args()

    a = args.name.replace("-"," ")
    url = "https://www.subfactory.fr/series.html&action=g_calendar"

    page_calendar = Page(url)
    if args.c :
        soup = bs(page_calendar.html,'html.parser')
        print(get_quick_calendar(soup, a))

    page_info = Page(url)
    if args.pv:
        soup = bs(page_info.html, "html.parser")
        print(get_quick_info_serie(soup, a))










