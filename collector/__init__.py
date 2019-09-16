# UrlManager
from urllib.request import urlopen
from urllib.parse import urljoin

# crawler
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

import requests
import re



class UrlManager:
    def __init__(self, domain="http://www.itworld.co.kr/"):
        self.domain = domain
        self.paths = {
            'main': 'main/'
        }

    def get(self, path, is_alias=False):
        if is_alias:
            return urljoin(self.domain, self.paths.get(path, path))
        elif isinstance(path, (list, tuple)):
            return urljoin(self.domain, *path)
        else:
            return urljoin(self.domain, path)


class NewsCollector:
    def __init__(self):
        self.UrlManager = UrlManager()
        self.articles = {}
        self.today = datetime.now()

    ##########
    #scraping#
    ##########
    def get_html(self, url):
        res = requests.get(url)

        if not res.ok:
            raise Exception('connection error')

        return res
    
    def parse_response_to_bs(self, response, features='html.parser'):
        return BeautifulSoup(response.text, features)
    
    def get_element_by_css(self, bs_page, css_selector):
        return bs_page.select_one(css_selector)
    
    def get_elements_by_css(self, bs_page, css_selector):
        return bs_page.select(css_selector)
    
    ######
    #util#
    ######
    def format_date(self, dt):
        if re.search("분 전$", dt):
            return self.today - timedelta(minutes=int(dt[:-3]))
        elif re.search("시간 전$", dt):
            return self.today - timedelta(hours=int(dt[:-4]))
        elif re.search("일 전$", dt):
            return self.today - timedelta(days=int(dt[:-3]))
        else:
            return datetime.strptime(dt, "%Y.%m.%d")
    
    ######
    #main#
    ######
    def collect_latest(self, path="main"):
        """최신 기사 크롤링"""
        url = self.UrlManager.get(path, is_alias=True)
        main_page = self.get_html(url)
        main_page = self.parse_response_to_bs(main_page)
        
        self.articles['latest'] = []
        latest_articles = self.get_elements_by_css(
            main_page,
            "body > div:nth-child(6) > div.body_ > div.body_left > div:nth-child(1) > div:nth-child(2) > div > ul > li"
        )
        
        for latest_article in latest_articles:
            a = self.get_element_by_css(latest_article, "div:nth-child(1) > a")
            date = self.get_element_by_css(latest_article, "div:nth-child(2)").text.strip()
            date = self.format_date(date)

            self.articles['latest'].append({
                'date': date.strftime("%Y-%m-%d"),
                'title': a.text,
                'content': self.collect_news_content(a.attrs.get('href')),
                'url': a.attrs.get('href'),
            })
    
    def collect_main(self, path="main"):
        """주요 기사 크롤링"""
        url = self.UrlManager.get(path, is_alias=True)
        main_page = self.get_html(url)
        main_page = self.parse_response_to_bs(main_page)
        
        self.articles['main'] = []
        main_articles = self.get_elements_by_css(
            main_page,
            '#main_top_news_list > div'
        )

        for main_article in main_articles:
            title = main_article.select_one('.news_list_title')
            url = title.select_one('a').attrs.get('href')
            title = title.attrs.get('title')
            theme_dt = main_article.select_one('.of-h.cb')
            themes = main_article.select('.news_list_source > a')
            themes = [
                {
                    'name': theme.text,
                    'url': theme.attrs.get('href')
                } for theme in themes
            ]
            dt = main_article.select_one('.news_list_time').text.strip()

            self.articles['main'].append({
                'title': title,
                'content': self.collect_news_content(url),
                'themes': themes,
                'date': self.format_date(dt).strftime("%Y-%m-%dT%H:%M:%S"),
                'url': url
            })
    
    def collect_news_content(self, news_url):
        # url 예외상황 처리
        news_url = self.UrlManager.get(news_url)
        # 변수 설정
        detail_page_num = 0
        is_one_page = False
        content = ""

        while True:
            detail_res = self.get_html(news_url + f"?page=0,{detail_page_num}")
            detail_page_num += 1
            detail_bs = self.parse_response_to_bs(detail_res)

            # 첫번째 pagination 제거
            pagination = self.get_element_by_css(detail_bs, ".pagination.pagination")

            # pagination 존재 == 2장 이상 뉴스
            if pagination:
                pagination.extract()

                # 두번째 안보이는 pagination에서 마지막 페이지 정보 얻기
                pagination = self.get_element_by_css(detail_bs, ".pagination.pagination").extract()
                pagination = self.get_elements_by_css(pagination, "li")

                # 페이지 넘기면 break
                if detail_page_num == len(pagination):
                    break
            # pagination 없는 한페이지 뉴스
            else:
                is_one_page = True

            # 기사 내용 추출 (html 형태)
            detail_content = str(self.get_element_by_css(detail_bs, ".node_body.cb"))
            # 전처리
            detail_content = detail_content.strip()
            detail_content = detail_content.replace("\n", "<br>")
            detail_content = detail_content.replace("\xa0", "")
            detail_content = detail_content.replace('src="', 'src="http://www.itworld.co.kr/')
            detail_content = detail_content.replace("<br/>", "")
            detail_content = detail_content.replace("\t", "")
            detail_content = detail_content.replace("\r", "")

            # 최종 변수에 담기
            content += detail_content

            # pagination 없는 한페이지
            if is_one_page:
                break
        
        return content
        