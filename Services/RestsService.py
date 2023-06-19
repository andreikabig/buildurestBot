from DatabaseModels import Rest

class RestsService:
    @staticmethod
    def GetAllRestsText():
        rests = Rest.select()

        text = ""

        for rest in rests:
            text += f"{rest.id}. {rest.name}\nОписание: {rest.description}\nЦена от: {rest.price}\n" \
                    f"Тип отдыха: {rest.rest_type.name}\n\n"

        return text

    @staticmethod
    def GetRestById(id):
        try:
            return Rest.get(Rest.id == id)
        except:
            return None