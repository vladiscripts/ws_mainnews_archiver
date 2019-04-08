#!/usr/bin/env python
# coding: utf-8
import re
import pywikibot


def wiki_posting_page(page_obj, text_new, summary):
    if page_obj.text != text_new:
        page_obj.text = text_new
        page_obj.save(summary=summary)


if __name__ == '__main__':
    site = pywikibot.Site('ru', 'wikisource', user='TextworkerBot')
    news = pywikibot.Page(site, 'Викитека:Новости сайта')

    section = re.search('<section begin="news"[/ ]+>(.+?)\n?<section end="news"', news.text, flags=re.S).group(1)
    items = [f'\n* {i.strip()}' for i in section.split('\n*') if i.strip() != '']
    n = 10  # limit for number of rows
    if len(items) > n:
        news_new = news.text.replace(section, ''.join(items[:n]))
        excess = ''.join(items[n:])

        archname = re.search('<!--.*?бота-архиватора[:\s]*\[\[(.*?)\]\]\s*-->', news.text, flags=re.S).group(1)
        archpage = pywikibot.Page(site, archname)
        pretext = re.search('^(.*?)\n\*', archpage.text, flags=re.S)
        if pretext:
            pretext = pretext.group(1)
            archive_new = archpage.text.replace(pretext, f"{pretext}{excess}")

            wiki_posting_page(news, news_new, 'архивация')
            wiki_posting_page(archpage, archive_new, 'архивация')
