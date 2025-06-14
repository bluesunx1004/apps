from hanspell import spell_checker

text = "안녕하세요. 이것은 테스트 문장입니다."
try:
    result = spell_checker.check(text)
    checked_text = result.checked
except Exception as e:
    checked_text = text
    error_message = str(e)
    print(error_message)  # 또는 st.error(error_message) 등으로 출력
