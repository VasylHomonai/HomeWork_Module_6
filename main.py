from collections import UserDict
import traceback


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
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return True
        return False

    # Редагування тел. у користувача
    def edit_phone(self, old_number: str, new_number: str):
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                new_phone = Phone(new_number)
                self.phones[i] = new_phone
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


def main():
    try:
        # Створення нової адресної книги
        book = AddressBook()

        # Створення запису для John
        john_record = Record("John")
        # Додавання запису John до адресної книги
        book.add_record(john_record)
        # Додавання телефонів для John
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")
        john_record.add_phone("7777777777")
        # Знаходження телефона у John для заміни
        for old_num in ["3333333333", "7777777777"]:
            phone = john_record.find_phone(old_num)
            if phone:
                john_record.edit_phone(phone.value, "1111111111")
        # Знаходження телефона у John для видалення
        for del_num in ["7777777777", "1234567890"]:
            phone = john_record.find_phone(del_num)
            if phone:
                john_record.remove_phone(phone.value)

        # Виведення запису у тел. книзі
        print("Вивід доданого контакту:", book, end="\n\n")  # Вивід: Contact name: John, phones: 5555555555; 1111111111

        # Створення та додавання нового запису для Jane
        jane_record = Record("Jane")
        book.add_record(jane_record)
        # Додавання телефонів для Jane
        jane_record.add_phone("9876543210")
        jane_record.add_phone("9999999999")

        # Виведення записів у тел. книзі
        print("Вивід контактів після дод. нового:", book)    # Вивід: Contact name: John, phones: 5555555555; 1111111111
        #                                                             Contact name: Jane, phones: 9876543210; 9999999999
        print()
        # Знаходження контакту у тел. книзі book для видалення
        for name in ["Vasyl", "John"]:
            contact = book.find(name)
            if contact:
                book.delete(name)

        # Виведення записів у тел. книзі
        print("Виведення контактів після видалення:", book)  # Вивід: Contact name: Jane, phones: 9876543210;

    except (EmptyNameError, InvalidPhoneError) as e:
        print("Помилка:", e)
    except Exception as e:
        print("Загальна помилка:", e)
        traceback.print_exc()


if __name__ == "__main__":
    main()
