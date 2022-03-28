def code_added(code):
    return f"Ваш код {code} успешно зарегистрирован.\n" \
           f"Для получения джек-пота необходимо сохранить бабочку с кодом.\n" \
           f"Вся подробная информация будет на странице"


def greet():
    return "Здравствуйте, введите свой код с бабочки в виде:\n" \
           "/code XXXXX"


def invalid_code(code):
    return f"Введённый код {code} не валиден"


def empty_code():
    return f"После /code необхоимо указать код продукта:\n" \
           f"/code XXXXX"


def help_message():
    return "Введите свой код с бабочки в виде:\n " \
           "/code XXXXX"

