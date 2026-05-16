from dataclasses import dataclass


@dataclass(frozen=True)
class OrderUser:
    name: str
    surname: str
    address: str
    metro: str
    phone: str
    rental_period: str = "сутки"


ORDER_USERS = [
    OrderUser(
        name="Анна",
        surname="Смирнова",
        address="ул. Пушкина, 10",
        metro="Сокол",
        phone="+79991234567",
    ),
    OrderUser(
        name="Пётр",
        surname="Петров",
        address="пр. Мира, 5",
        metro="Черкизовская",
        phone="+79997654321",
        rental_period="двое суток",
    ),
]

# Разные точки входа: верхняя и нижняя кнопка «Заказать» на главной.
ORDER_ENTRY_POINTS = [
    "top",
    "bottom",
]
