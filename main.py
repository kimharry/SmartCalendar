import os
from dotenv import load_dotenv
from openai import OpenAI
from create_event import create_event
import argparse
import pytesseract
# import pykospacing

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("API key is not set")
client = OpenAI(api_key=OPENAI_API_KEY)

instruction = """다음의 양식을 사용하여 사용자 요청에 응답하세요. 불필요한 정보 없이 양식만 따르세요.
title: (이벤트의 제목)
start_date: (시작 날짜, 형식: YYYY-MM-DDTHH:MM:SS)
end_date: (종료 날짜, 형식: YYYY-MM-DDTHH:MM:SS)
location: (위치)

양식 외의 설명이나 추가적인 정보는 제공하지 않습니다."""

def get_event_text(email_text):
    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal::AaLVuMzw",
        messages=[
            { "role": "system", "content": instruction },
            { "role": "user", "content": email_text}
        ]
    )

    result = response.choices[0].message.content.strip()
    return result

def extract_email_text(path):
    text = pytesseract.image_to_string(path, lang="kor+eng")
    text = text.replace(" ", "")
    print(text)
    return text

def main():
    parser = argparse.ArgumentParser(description="Create an event from an email")
    parser.add_argument("--option", "-o", type=int, help="Input Option: 1 for text input, 2 for image input", required=True)
    parser.add_argument("--input", "-i", type=str, help="Image path", required=False)
    args = parser.parse_args()

    if args.option == 1:
        email_text = input("이메일 내용을 입력하세요: ")
    elif args.option == 2:
        email_text = extract_email_text(args.input)
    else:
        raise ValueError("Invalid option")
    
    event_text = get_event_text(email_text)
    
    print(event_text)
    check = input("이벤트를 생성하시겠습니까? (y/n): ")

    while True:
        if check.lower() == "y":
            create_event(event_text)
            break
        elif check.lower() == "n":
            print("이벤트 생성을 취소합니다.")
            break
        else:
            check = input("y 또는 n을 입력하세요: ")

if __name__ == "__main__":
    main()