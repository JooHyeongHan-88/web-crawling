import platform, psutil
import os
import logging
from bs4 import BeautifulSoup
import requests
import lxml


# 로거 생성
logger = logging.getLogger()

# 로그 출력 기준 설정
logger.setLevel(logging.INFO)

# 로그 양식 지정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(message)s')

# 로그 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log 파일 생성
file_handler = logging.FileHandler('output.log', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def print_system_info():
    logger.info(f'''
        OS                  :\t{platform.system()}
        OS Version          :\t{platform.version()}
        Process Information :\t{platform.processor()}
        Process Architecture:\t{platform.machine()}
        CPU Cores           :\t{os.cpu_count()}
        RAM Size            :\t{str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + "(GB)"}
    ''')


# 네이버 연합뉴스 URL
URL1 = 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&id1=100'
URL2 = 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&id1=101'
URL3 = 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&id1=102'
URL4 = 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&id1=103'
URL5 = 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&id1=104'
URL6 = 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&id1=105'


def web_crawler(url):
    # 헤더 설정
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.56'}

    # 서버 응답 확인
    response = requests.get(url, headers=headers)

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.content, 'lxml')

    # 페이지 제목 크롤링
    print(soup.title.string)

    # 기사 제목 크롤링
    print(soup.find("ul", attrs={"class": "type06_headline"}).get_text())


def main(cpu=3):
    from multiprocessing import Pool
    import time

    url_list = [URL1, URL2, URL3, URL4, URL5, URL6]

    logger.info(f"멀티 프로세스가 시작됩니다.")
    
    start_time = time.time()

    pool = Pool(processes=cpu)
    result = pool.map(web_crawler, url_list)

    pool.close()
    pool.join()

    logger.info(f"멀티 프로세스가 종료되었습니다.")
    logger.info("--- {} seconds ---".format(time.time() - start_time))


if __name__ == "__main__":
    import schedule
    import argparse

    print_system_info()

    # 매개변수 설정
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpu", type=int, default=3, help="멀티 프로세스 CPU 수")
    parser.add_argument("--run_interval", type=int, default=5, help="웹 크롤러 실행 주기(초)")

    args = parser.parse_args()
    
    cpu = args.cpu
    interval = args.run_interval

    logger.info(f'''
        CPU 사용         :\t{cpu} 코어
        프로그램 실행 주기:\t{interval} 초
    ''')

    # N초에 한번씩 메인 함수 실행하도록 설정정
    schedule.every(interval).seconds.do(main)

    # 스케쥴러 실행
    while True:
        schedule.run_pending()