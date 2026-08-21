import os
import random
from datetime import datetime
import google.generativeai as genai

# 🚨 비밀금고 접근 권한
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def load_keywords(filename="keywords.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            keywords = [line.strip() for line in f.readlines() if line.strip()]
        return keywords
    except FileNotFoundError:
        print(f"🚨 에러: {filename} 파일이 없습니다!")
        exit(1)

def generate_dynamic_toc(model, keyword):
    # 🧠 [Step 1] AI에게 키워드 맞춤형 목차를 짜오라고 지시!
    print(f"🔍 '{keyword}' 맞춤형 목차 기획 중...")
    prompt = f"""
    너는 스페셜티 커피 전문 마케터야.
    사람들이 구글에 '{keyword}'를 검색하는 진짜 의도를 파악해서,
    가장 클릭하고 싶고 유용한 블로그 목차 3개를 작성해.
    
    [🚨 규칙]
    - 반드시 1. 2. 3. 번호로 시작할 것.
    - 다른 군더더기 인사말 없이 딱 목차 3줄만 출력할 것.
    - 디카페인 관련 내용은 절대 포함하지 말 것.
    """
    toc = model.generate_content(prompt).text.strip()
    return toc

def write_blog_post(model, keyword, dynamic_toc):
    # ✍️ [Step 2] AI가 스스로 짠 목차를 바탕으로 본문 작성!
    print(f"✍️ 기획된 목차를 바탕으로 블로그 본문 작성 중...")
    prompt = f"""
    너는 스페셜티 커피 브랜드 '아임유어커피'의 수석 로스터야.
    주제: '{keyword}'
    
    [🚨 엄격한 작성 규칙]
    1. 반드시 아래의 [맞춤형 목차] 흐름에 따라 글을 작성해.
    2. 특수문자 숫자 이모지(1️⃣, 2️⃣) 절대 금지! 일반 텍스트(1., 2.)만 써.
    3. 디카페인 커피에 대한 언급은 절대 금지!
    4. 타사 브랜드 비하 금지, 객관적이고 고급스러운 정보 전달.
    
    [맞춤형 목차]
    {dynamic_toc}
    """
    return model.generate_content(prompt).text

def save_post(keyword, content):
    today = datetime.now().strftime("%Y-%m-%d")
    # 파일명에 공백이 들어갈 수 있으니 안전하게 변환
    safe_keyword = keyword.replace(" ", "-")
    filename = f"{today}-{safe_keyword}.md"
    
    top_image = "![아임유어커피](https://images.unsplash.com/photo-1497935586351-b67a49e012bf?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80)\n\n"
    
    cta_link = f"""\n\n---
### ☕ 나만의 공간을 완벽한 카페로
오늘 알게 된 커피 꿀팁, 최고급 스페셜티 원두로 직접 경험해 보세요.
당신의 취향을 완벽하게 저격할 한 잔, **'아임유어커피'**가 곧 찾아옵니다.
"""
    final_content = top_image + content + cta_link
    front_matter = f"---\nlayout: post\ntitle: '{keyword} - 수석 로스터가 알려주는 완벽 가이드'\ndate: {today}\n---\n\n"
    
    os.makedirs("_posts", exist_ok=True)
    with open(f"_posts/{filename}", "w", encoding="utf-8") as f:
        f.write(front_matter + final_content)
    print(f"🚀 [성공] '{keyword}' 맞춤형 포스팅 완료!")

if __name__ == "__main__":
    if not GEMINI_API_KEY:
        print("🚨 에러: API 키가 없습니다!")
        exit(1)
        
    model = genai.GenerativeModel('gemini-3.5-flash')
    
    # 1. 280개 키워드 리스트 로드
    keyword_list = load_keywords()
    
    # 2. 오늘의 타겟 키워드 랜덤 선택
    target_keyword = random.choice(keyword_list)
    print(f"🤖 오늘 아임유어커피 봇의 타겟: {target_keyword}")
    
    # 3. 맞춤형 목차 생성 (투스텝 작전 1)
    custom_toc = generate_dynamic_toc(model, target_keyword)
    print(f"📋 [생성된 맞춤형 목차]\n{custom_toc}")
    
    # 4. 본문 작성 및 저장 (투스텝 작전 2)
    content = write_blog_post(model, target_keyword, custom_toc)
    save_post(target_keyword, content)
    print("✅ 투스텝 동적 뇌구조 포스팅 완료!")
