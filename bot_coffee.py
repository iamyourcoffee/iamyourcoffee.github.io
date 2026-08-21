import os
from datetime import datetime
import google.generativeai as genai

# 🚨 비밀금고 접근 권한
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# 🎯 타겟 키워드 세팅
KEYWORD = "홈카페 원두 추천"

def write_blog_post(keyword):
    model = genai.GenerativeModel('gemini-3.5-flash')
    prompt = f"""
    너는 바리스타이자 커피 전문 블로거야. 검색어 '{keyword}'를 주제로 블로그 글을 작성해 줘.
    
    [🚨 엄격한 작성 규칙]
    1. 반드시 아래 지정된 3가지 목차로만 글을 구성해.
    2. 1️⃣, 2️⃣ 같은 '특수문자 숫자 이모지' 절대 금지! 일반 텍스트(1., 2.)만 써.
    
    [지정 목차]
    ## 1. 나만의 홈카페, 어떤 원두로 시작할까?
    ## 2. 실패 없는 홈카페 원두 고르는 꿀팁
    ## 3. 원두 보관법과 최고의 맛을 내는 추출법
    """
    response = model.generate_content(prompt)
    return response.text

def save_post(keyword, content):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-coffee-post.md"
    
    # 향긋한 커피 테마 고화질 이미지 주입
    top_image = "![커피 원두](https://images.unsplash.com/photo-1559525839-b184a4d698c7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80)\n\n"
    
    # (나중에 스마트스토어 링크 나오면 여기에 추가할 예정!)
    cta_link = f"""\n\n---
### ☕ 매일 아침을 깨우는 완벽한 커피 한 잔
당신의 취향에 딱 맞는 스페셜티 원두로 나만의 완벽한 홈카페를 완성해 보세요.
"""
    final_content = top_image + content + cta_link
    front_matter = f"---\nlayout: post\ntitle: '{keyword}: 나만의 완벽한 홈카페 만들기'\ndate: {today}\n---\n\n"
    
    os.makedirs("_posts", exist_ok=True)
    with open(f"_posts/{filename}", "w", encoding="utf-8") as f:
        f.write(front_matter + final_content)
    print(f"🚀 [성공] 아임유어커피 1호기 전용 {filename} 파일 생성 완료!")

if __name__ == "__main__":
    if not GEMINI_API_KEY:
        print("🚨 에러: API 키가 없습니다!")
        exit(1)
    print("🤖 커피 봇 1호기 작동 시작...")
    post_content = write_blog_post(KEYWORD)
    save_post(KEYWORD, post_content)
    print("✅ 1호기 커피 포스팅 장착 완료!")
