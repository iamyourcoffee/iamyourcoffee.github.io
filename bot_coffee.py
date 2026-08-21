import os
import requests
import json
import random
from datetime import datetime
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

RECIPE_SEEDS = [
    "홈카페 바닐라라떼 만들기", "아인슈페너 크림 비율", "스타벅스 돌체라떼 레시피",
    "홈카페 카라멜 마끼아또", "콜드브루 라떼 레시피", "카페모카 홈카페",
    "흑임자 크림 라떼 만들기", "아포가토 레시피", "얼그레이 샷추가 레시피",
    "연유라떼 홈카페 비율"
]

def get_longtail_keyword(base_keyword):
    print(f"🔍 구글 검색창에서 '{base_keyword}' 연관 레시피 롱테일 크롤링 중...")
    try:
        url = f"http://suggestqueries.google.com/complete/search?client=chrome&q={base_keyword}"
        response = requests.get(url)
        suggestions = json.loads(response.text)[1]
        
        banned_words = ["디카페인", "원두", "구독", "납품", "도매"]
        filtered = [s for s in suggestions if not any(b in s for b in banned_words)]
        
        return filtered[-1] if filtered else base_keyword
    except:
        return base_keyword

def generate_dynamic_toc(model, keyword):
    prompt = f"""
    너는 홈카페 레시피 전문 크리에이터야.
    '{keyword}'를 검색한 사람들이 집에서 똑같이 따라 만들 수 있도록 완벽한 레시피 목차 3개를 기획해.
    
    [🚨 규칙]
    - 1. 필요한 재료 소개 2. 황금 비율 레시피 과정 3. 맛있게 즐기는 꿀팁 (이 흐름으로 작성)
    - 반드시 1. 2. 3. 번호로 시작하고, 딱 목차 3줄만 출력할 것.
    - 로스팅, 원두의 맛, 산미, 숙성, 가스 배출 같은 전문가적인 원두 이야기는 절대 금지.
    """
    return model.generate_content(prompt).text.strip()

def write_blog_post(model, keyword, dynamic_toc):
    prompt = f"""
    너는 누구나 따라 하기 쉬운 홈카페 음료 레시피를 전하는 블로거야.
    주제: '{keyword}'
    
    [🚨 엄격한 작성 규칙]
    1. 아래 [맞춤형 레시피 목차]에 따라 재료, 용량(ml, g), 만드는 순서 위주로 작성해.
    2. 특수문자 숫자 이모지(1️⃣, 2️⃣) 절대 금지! 일반 텍스트(1., 2.)만 써.
    3. 원두 판매, 정기 구독, 로스팅 날짜, 200g 소포장 같은 비즈니스 및 원두 관련 이야기는 철저하게 배제해. 오직 '음료를 맛있게 만드는 법'에만 집중해!
    
    [맞춤형 레시피 목차]
    {dynamic_toc}
    """
    return model.generate_content(prompt).text

def save_post(keyword, content):
    today = datetime.now().strftime("%Y-%m-%d")
    safe_keyword = keyword.replace(" ", "-")
    filename = f"{today}-{safe_keyword}.md"
    
    top_image = "![홈카페 레시피](https://images.unsplash.com/photo-1497935586351-b67a49e012bf?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80)\n\n"
    
    # 🚨 사령관님 하명대로 시크하게 딱 한 줄 + 링크!
    cta_link = f"""\n\n---
-당신이 찾던 원두, 아임유어커피-
**[👉 https://smartstore.naver.com/iamyourcoffee](https://smartstore.naver.com/iamyourcoffee)**
"""
    final_content = top_image + content + cta_link
    front_matter = f"---\nlayout: post\ntitle: '{keyword} - 집에서 즐기는 완벽한 홈카페 레시피'\ndate: {today}\n---\n\n"
    
    os.makedirs("_posts", exist_ok=True)
    filepath = f"_posts/{filename}"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(front_matter + final_content)
    print(f"🚀 [성공] 레시피 파일 생성 완료: {filepath}")
    return filepath

if __name__ == "__main__":
    model = genai.GenerativeModel('gemini-3.5-flash')
    
    target_keyword = random.choice(RECIPE_SEEDS)
    print(f"🤖 타겟 레시피 시드: {target_keyword}")
    
    longtail_keyword = get_longtail_keyword(target_keyword)
    print(f"🎯 최종 롱테일 레시피 키워드: {longtail_keyword}")
    
    custom_toc = generate_dynamic_toc(model, longtail_keyword)
    print(f"📋 [기획된 레시피 목차]\n{custom_toc}")
    
    content = write_blog_post(model, longtail_keyword, custom_toc)
    filepath = save_post(longtail_keyword, content)
    
    with open("last_test_file.txt", "w") as f:
        f.write(filepath)
