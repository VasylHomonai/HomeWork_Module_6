from collections import UserDict


class EmptyNameError(ValueError):
    pass


class InvalidPhoneError(ValueError):
    pass


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name: str):
        if name is None or name.strip() == "":
            raise EmptyNameError("Ім'я є обов'язковим полем і не може бути порожнім.")
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone: str):
        # Якщо тел. буде передано наприклад в такому форматі "000-123-45-67" то змінемо формат на "0001234567"
        digits = ''.join(filter(str.isdigit, str(phone)))
        if len(digits) != 10:
            raise InvalidPhoneError("Номер телефону має містити 10 цифр.")
        super().__init__(digits)


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    # Додавання тел. користувачеві
    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        self.phones.append(phone)

    # Видалення тел. у користувача
    def remove_phone(self, phone_number: str):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
            return True
        return False

    # Редагування тел. у користувача
    def edit_phone(self, old_number: str, new_number: str):
        # Додавання нового тел. в кінець списку, без врахування порядку
        if self.find_phone(old_number):
            self.remove_phone(old_number)
            self.add_phone(new_number)
        # Якщо важливий порядок, щоб новий тел. стояв на міці старого, то реалізація:
        # phone = self.find_phone(old_number)
        # if phone:
        #     index = self.phones.index(phone)
        #     self.phones[index] = Phone(new_number)
            return True
        raise InvalidPhoneError(f"Телефонний номер {old_number} не знайдено")

    # Пошук тел. у списку тел. користувача
    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    # Інформативне представлення поточного стану об'єкта
    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        # record — це екземпляр класу Record (користувач з телефонами)
        # Ключем у словнику буде Ім'я(record.name.value) а значенням сам об'єкт record
        self.data[record.name.value] = record

    # Пошук за іменем у телефонній книзі користувача з тел.
    def find(self, name: str):
        return self.data.get(name)

    # Видалення об'єкта класу Record, тобто видаляє користувача з телефонами
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
            return True
        return False

    # Інформативне представлення поточного стану об'єкта
    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
