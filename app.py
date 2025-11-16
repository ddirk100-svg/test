from flask import Flask, request, render_template, jsonify, session, redirect, url_for
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from functools import wraps

# 환경변수 로드
load_dotenv()

# API 키 설정
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
OPENAI_KEY = os.getenv("OPENAI_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_KEY)

# Supabase 클라이언트 초기화
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

# Flask session 설정
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'

# 네이버 뉴스 API URL
NAVER_URL = "https://openapi.naver.com/v1/search/news.json"


# 캐시 방지 데코레이터
def no_cache(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        if hasattr(response, 'headers'):
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response
    return decorated_function


# 로그인 필수 데코레이터
def login_required(f):
    @wraps(f)
    @no_cache
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


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
@no_cache
def home():
    """홈페이지 - 검색창 표시"""
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """회원가입"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # 입력 검증
        if not email or not password:
            return render_template('register.html', error="이메일과 비밀번호를 입력해주세요.")
        
        if password != password_confirm:
            return render_template('register.html', error="비밀번호가 일치하지 않습니다.")
        
        if len(password) < 6:
            return render_template('register.html', error="비밀번호는 최소 6자 이상이어야 합니다.")
        
        try:
            # Supabase Auth로 회원가입 시도
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                # identities가 비어있으면 이미 존재하는 이메일
                if hasattr(response.user, 'identities') and not response.user.identities:
                    return render_template('register.html', error=f"이미 가입된 이메일입니다. ({email})")
                
                # 회원가입 성공
                return render_template('register_success.html', email=email)
            else:
                return render_template('register.html', error="회원가입에 실패했습니다. 다시 시도해주세요.")
                
        except Exception as e:
            error_msg = str(e).lower()
            
            # 중복 이메일 에러 체크
            if any(keyword in error_msg for keyword in ['already registered', 'already exists', 'duplicate', 'unique']):
                return render_template('register.html', error=f"이미 가입된 이메일입니다. ({email})")
            elif 'invalid' in error_msg and 'email' in error_msg:
                return render_template('register.html', error="유효하지 않은 이메일 형식입니다.")
            else:
                return render_template('register.html', error="회원가입에 실패했습니다. 다시 시도해주세요.")
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """로그인"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # 입력 검증
        if not email or not password:
            return render_template('login.html', error="이메일과 비밀번호를 입력해주세요.")
        
        try:
            # Supabase Auth로 로그인
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                # 로그인 성공 - 세션에 사용자 정보 저장
                session['user_id'] = response.user.id
                session['user_email'] = response.user.email
                
                # next 파라미터가 있으면 해당 페이지로, 없으면 홈으로
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error="로그인에 실패했습니다.")
                
        except Exception as e:
            error_msg = str(e)
            if 'invalid' in error_msg.lower() or 'credentials' in error_msg.lower():
                return render_template('login.html', error="이메일 또는 비밀번호가 올바르지 않습니다.")
            else:
                print(f"로그인 오류: {e}")
                return render_template('login.html', error="로그인에 실패했습니다. 다시 시도해주세요.")
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """로그아웃"""
    try:
        # Supabase 로그아웃
        supabase.auth.sign_out()
    except:
        pass
    
    # 세션 클리어
    session.clear()
    
    # 캐시 방지 헤더와 함께 리다이렉트
    response = redirect(url_for('home'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/search')
@login_required
def search():
    """검색 결과 페이지 - 뉴스 검색 및 요약"""
    keyword = request.args.get('query', '').strip()
    display = request.args.get('display', '5')
    user_id = session.get('user_id')  # 로그인한 사용자 ID
    
    # 검색어 유효성 검사
    if not keyword:
        return render_template('home.html', error="검색어를 입력해주세요.")
    
    # display 값 검증 (1~10 사이)
    try:
        display_count = int(display)
        display_count = max(1, min(10, display_count))  # 1~10 범위로 제한
    except ValueError:
        display_count = 5  # 기본값
    
    # 네이버 뉴스 검색
    items = search_naver_news(keyword, display=display_count)
    
    if not items:
        return render_template('results.html', keyword=keyword, items=[], error="검색 결과가 없습니다.", user_id=user_id)
    
    # 각 뉴스에 AI 요약 추가
    for item in items:
        description = item.get("description", "")
        if description:
            item["summary"] = summarize_text(description)
        else:
            item["summary"] = "요약할 내용이 없습니다."
    
    return render_template('results.html', keyword=keyword, items=items, error=None, user_id=user_id)


@app.route('/favorites')
@login_required
def favorites():
    """즐겨찾기 목록 페이지"""
    user_id = session.get('user_id')
    
    try:
        # Supabase에서 즐겨찾기 조회
        response = supabase.table('favorites').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
        items = response.data
        
        return render_template('favorites.html', items=items, user_id=user_id)
    
    except Exception as e:
        print(f"즐겨찾기 조회 오류: {e}")
        return render_template('favorites.html', items=[], error="즐겨찾기를 불러올 수 없습니다.", user_id=user_id)


@app.route('/api/favorites/add', methods=['POST'])
@login_required
def add_favorite():
    """즐겨찾기 추가 API"""
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        
        # 필수 필드 검증
        required_fields = ['title', 'link']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': '필수 정보가 누락되었습니다.'}), 400
        
        # Supabase에 저장
        favorite_data = {
            'user_id': user_id,
            'title': data['title'],
            'description': data.get('description', ''),
            'summary': data.get('summary', ''),
            'link': data['link']
        }
        
        response = supabase.table('favorites').insert(favorite_data).execute()
        
        return jsonify({'success': True, 'message': '즐겨찾기에 추가되었습니다.', 'data': response.data})
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        if 'duplicate' in error_msg.lower() or 'unique' in error_msg.lower():
            return jsonify({'success': False, 'message': '이미 즐겨찾기에 추가된 기사입니다.'}), 409
        
        print(f"즐겨찾기 추가 오류: {e}")
        print(f"상세 에러:\n{error_trace}")
        return jsonify({'success': False, 'message': f'즐겨찾기 추가에 실패했습니다: {error_msg}'}), 500


@app.route('/api/favorites/remove', methods=['POST'])
@login_required
def remove_favorite():
    """즐겨찾기 삭제 API"""
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        link = data.get('link')
        
        if not link:
            return jsonify({'success': False, 'message': '필수 정보가 누락되었습니다.'}), 400
        
        # Supabase에서 삭제
        response = supabase.table('favorites').delete().eq('user_id', user_id).eq('link', link).execute()
        
        return jsonify({'success': True, 'message': '즐겨찾기에서 제거되었습니다.'})
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"즐겨찾기 삭제 오류: {e}")
        print(f"상세 에러:\n{error_trace}")
        return jsonify({'success': False, 'message': f'즐겨찾기 삭제에 실패했습니다: {str(e)}'}), 500


if __name__ == '__main__':
    # 한글 인코딩 설정
    app.config['JSON_AS_ASCII'] = False
    
    # 로컬 개발 환경
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
