from chat_service import answer_question

#sum = 0
#for num in range(1,11):
#    sum += num
#    print(sum)
#print(f"1부터 10까지의 총합 : {sum}")


while True:
    question = input("질문 (종료: q): ")

    if question.strip().lower() in ("q", "quit", "exit", "종료"):
        print("대화를 종료합니다.")
        break

    if not question.strip():
        continue

    answer = answer_question(question)
    print("답변:", answer)
    print()
#question = input("질문: ")
#answer = answer_question(question)
#print ("답변:", answer)

