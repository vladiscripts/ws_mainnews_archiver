#!/usr/bin/env python
# coding: utf-8
import re
import pywikibot


def posting(page_obj, text_new, summary):
    if page_obj.text != text_new:
        page_obj.text = text_new
        page_obj.save(summary=summary)


def get_wikipage(site, name):
    page = pywikibot.Page(site, name)
    while page.isRedirectPage():
        page = page.getRedirectTarget()
    return page


if __name__ == '__main__':
    site = pywikibot.Site('ru', 'wikisource', user='TextworkerBot')
    news_page = get_wikipage(site, 'Заглавная страница/Новости сайта')

    # Тег <section> плохо работает с ПИ Викитека, см. [[ВТ:ЗКА#Защита форумов до автоподтверждённых]],
    # также проблемы с <includeonly>. Поэтому — <noinclude>:
    # news_section = re.search('<section begin="news"[/ ]+>(.+?)\n?<section end="news"', news.text, flags=re.S).group(1)
    news_section = re.search(r'</noinclude>\s*(\*.+?)\s*<noinclude>', news_page.text, flags=re.S).group(1)
    items = re.findall(r'^(\*.+)$', news_section, flags=re.MULTILINE)
    n = 10  # limit for number of rows on the News page
    if len(items) > n:
        news_new = news_page.text.replace(news_section, '\n'.join(items[:n]))
        surplus = '\n'.join(items[n:])

        arch_name = re.search(r'archive_page\s*=\s*\[\[(.*?)\]\]', news_page.text, flags=re.S).group(1)
        arch_page = get_wikipage(site, arch_name)
        pretext = re.search(r'^(.*?)(?:\n\*)', arch_page.text, flags=re.S)
        if pretext:
            pretext = pretext.group(1)
            archive_new = arch_page.text.replace(pretext, f"{pretext}\n{surplus}")

            posting(news_page, news_new, 'архивация')
            posting(arch_page, archive_new, 'архивация')
