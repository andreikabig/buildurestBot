import random

import openai
from Services.RestsService import RestsService

openai.api_key = "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"

class AutoPickUpService:

    @staticmethod
    def PickUp(user):
        if user.about is None or user.about == "":
            return "Вы еще не заполнили информацию о себе, к сожалению, автоматический подбор не доступен.\n" \
                   "Пожалуйста, заполните информацию о себе через команду /about. Спасибо!"

        try:
            about = user.about

            rests = RestsService.GetAllRestsText()

            splits = rests.split("\n\n")
            count = 4
            restsChoice = ""

            for i in range(count):
                rand = random.randint(0, len(splits)-1)
                restsChoice += splits[rand]

            # задаем модель и промпт
            model_engine = "text-davinci-003"
            prompt = f"Имеются следующие активности, у каждой активности есть id (цифра с точкой в начале)." \
                     f"Вот описание пользователя: {about}." \
                     f"Вот активности: {restsChoice}." \
                     f"Твоя задача: написать только id (цифру), больше ничего, активности, которая больше подходит этому пользователю, активность должна быть одна."

            # задаем макс кол-во слов
            max_tokens = 128

            # генерируем ответ
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # выводим ответ
            answer = completion.choices[0].text
            print(answer)
            id = int(answer.strip(".").strip(" "))
            print(id)

            rest = RestsService.GetRestById(id)

            if rest is not None:
                return f"Мы считаем, что вам подойдет следующий отдых:\n" \
                       f"{rest.name}\nОписание: {rest.description}\nЦена от: {rest.price}\n" \
                       f"Тип отдыха: {rest.rest_type.name}\n\n"
            else:
                return "Что-то пошло не так, попробуйте чуть позже."
        except:
            return "Что-то пошло не так, попробуйте чуть позже."

