import os
from openai import OpenAI

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)

instruction = """다음의 양식을 사용하여 사용자 요청에 응답하세요. 불필요한 정보 없이 양식만 따르세요.
title: (이벤트의 제목)
start_date: (시작 날짜, 형식: YYYY-MM-DD)
end_date: (종료 날짜, 형식: YYYY-MM-DD)
location: (위치)

양식 외의 설명이나 추가적인 정보는 제공하지 않습니다."""""

response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:personal::AaLVuMzw",
    messages=[
        { "role": "system", "content": instruction },
        { "role": "user", "content": '안녕하세요. RC교육센터입니다. RC교육센터에서는 1년 RC교육 활동을 정리하고, RC Triple Advising 정규면담, RC교육프로그램 운영을 위해 RC미리메리크리스마스를 계획하여 운영할 예정입니다. 행사 운영 및 준비로 인해 테슬라커뮤니티센터 및 교내식당 이용에 불편이 있을 수 있으니 구성원들의 너른 양해 부탁드립니다. -행사명: 2024 RC미리메리크리스마스 -행사장소: 테슬라커뮤니티센터 및 구내식당 -행사일시: 2024. 11. 27.(수) 18:00 ~ 23:00 -행사내용: RC Triple Advising 정기면담(Professor\'s Table), e-Sports Day 결승전, 대외 표창장 수여식, 트리점등식 등 -주요사항: 교내식당 식사는 18:30분 이전까지 이용 가능 11. 26.(화) ~ 7.(수), 양일 간 테슬라커뮤니티센터 로비 및 벙커 내 행사 물품 설치로 인해 소음과 소란이 발생할 수 있음' }
    ]
)

print(response.choices[0].message.content.strip())