from flask import Flask, request, render_template
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# API 키 설정
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_KEY)

app = Flask(__name__)

# 네이버 뉴스 API URL
NAVER_URL = "https://openapi.naver.com/v1/search/news.json"


def search_naver_news(keyword, display=5):
    """
    네이버 뉴스 API를 호출하여 검색 결과를 반환합니다.
    
    Args:
        keyword (str): 검색 키워드
        display (int): 검색 결과 개수 (기본값: 5)
    
    Returns:
        list: 뉴스 아이템 리스트
    """
    try:
        headers = {
            "X-Naver-Client-Id": CLIENT_ID,
            "X-Naver-Client-Secret": CLIENT_SECRET
        }
        params = {
            "query": keyword,
            "display": display,
            "sort": "sim"  # 관련순 정렬
        }
        
        response = requests.get(NAVER_URL, headers=headers, params=params)
        response.raise_for_status()  # HTTP 에러 체크
        
        data = response.json()
        return data.get("items", [])
    
    except requests.exceptions.RequestException as e:
        print(f"네이버 API 호출 오류: {e}")
        return []


def summarize_text(text):
    """
    OpenAI GPT를 사용하여 텍스트를 한 문장으로 요약합니다.
    
    Args:
        text (str): 요약할 텍스트
    
    Returns:
        str: 요약된 문장
    """
    try:
        # HTML 태그 제거
        import re
        clean_text = re.sub('<[^<]+?>', '', text)
        
        prompt = f"다음 뉴스를 한 문장으로 아주 간단하고 명확하게 요약해줘:\n\n{clean_text}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=80
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"요약 생성 오류: {e}")
        return "요약을 생성할 수 없습니다."


@app.route('/')
def home():
    """홈페이지 - 검색창 표시"""
    return render_template('home.html')


@app.route('/search')
def search():
    """검색 결과 페이지 - 뉴스 검색 및 요약"""
    keyword = request.args.get('query', '').strip()
    
    # 검색어 유효성 검사
    if not keyword:
        return render_template('home.html', error="검색어를 입력해주세요.")
    
    # 네이버 뉴스 검색
    items = search_naver_news(keyword)
    
    if not items:
        return render_template('results.html', keyword=keyword, items=[], error="검색 결과가 없습니다.")
    
    # 각 뉴스에 AI 요약 추가
    for item in items:
        description = item.get("description", "")
        if description:
            item["summary"] = summarize_text(description)
        else:
            item["summary"] = "요약할 내용이 없습니다."
    
    return render_template('results.html', keyword=keyword, items=items, error=None)


if __name__ == '__main__':
    # 한글 인코딩 설정
    app.config['JSON_AS_ASCII'] = False
    
    # 로컬 개발 환경
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
