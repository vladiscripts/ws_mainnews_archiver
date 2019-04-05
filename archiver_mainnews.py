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
    archpage4 = pywikibot.Page(site, 'Викитека:Форум/Новости/Архив-4')

    section = re.search('<section begin="news"[/ ]+>(.+?)\n?<section end="news"', news.text, flags=re.S).group(1)
    items = [f'\n* {i.strip()}' for i in section.split('\n*') if i.strip() != '']
    n = 10  # limit for number of rows

    news_new = news.text.replace(section, ''.join(items[:n]))
    archive_new = re.sub('({{[Зз]акрыто.*?}})\n*', r'\1%s\n' % ''.join(items[n:]), archpage4.text, flags=re.S)

    wiki_posting_page(news, news_new, 'архивация')
    wiki_posting_page(archpage4, archive_new, 'архивация')
