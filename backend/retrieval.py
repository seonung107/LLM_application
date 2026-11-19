from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

def load_chunks():
    chunks = [] #문단을 담을 빈 목록
    # data 폴더의 TXT 파일을 하나씩 읽습니다.
    for path in sorted(DATA_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        #다음 슬라이드 코드를 이 아래에 이어 씁니다.
        # 빈 줄을 기준으로 문단을 나눈다.
        for paragraph in text.split("\n\n"):
            paragraph = paragraph.strip()
            if paragraph: #비어 있지 않은 문단만 저장
                chunks.append({
                    "source": path.name, #원본 파일명
                    "text" : paragraph, #문단 내용
                })
    return chunks 

#사용자정의 함수 추가
def make_words(text):
    # 대문자를 소문자로 통일합니다.
    cleaned = text.lower()
    # 문장부호를 공백으로 바꿉니다.
    for mark in "?!,./:()-":
        cleaned = cleaned.replace(mark, " ")
    # 공백을 기준으로 단어 목록을 만듭니다.
    return cleaned.split()

#사용자정의 함수 추가
def find_chunks(question):
    # 질문을 단어 목록으로 바꿉니다.
    question_words = make_words(question)
    found = []
    for chunk in load_chunks():
        content_words = make_words(chunk["text"])
        for word in question_words:
            # 같은 단어가 있으면 이 문단을 저장합니다.
            if len(word) > 1 and word in content_words:
                found.append(chunk)
                break  # 같은 문단은 한 번만 저장
        if len(found) == 3:
            break  # 세 문단을 찾았으면 검색 종료
    return found
