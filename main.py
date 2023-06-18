import re
import csv

## Читаем адресную книгу в формате CSV в список contacts_list:
def read_phonebook():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        return(contacts_list)

## 1. Выполните пункты 1-3 задания.
## Ваш код
def search_full_name(contacts_list):
    pattern = r"^([а-яА-ЯёЁ]+)(\s|,)([а-яА-ЯёЁ]+)?(\s|,)?([а-яА-ЯёЁ]+)?(\s|,)?"
    pattern_sub = r"\1 \3 \5 "
    lastname = []
    firstname = []
    surname = []
    for n in contacts_list:
        date = ",".join(list(n))
        sub_full_name = re.sub(pattern, pattern_sub, date)
        search_full_name = re.findall(pattern, sub_full_name)
        if len(search_full_name) != 0:
            full_name = (("".join(list(search_full_name[0]))).split(" ")[:3])
            lastname.append(full_name[0])
            firstname.append(full_name[1])
            surname.append(full_name[2])
    return(lastname, firstname, surname)

def search_email(contacts_list):
    pattern = r"([\w.]+\@\w+\.\w+)"
    email = []
    for i in contacts_list:
        email_adress = re.findall(pattern, ",".join(list(i)))
        if len(email_adress) != 0:
            email.append(email_adress[0])
        else:
            email.append("")
    email.pop(0)
    return(email)

def search_and_sub_phone(contacts_list):
    pattern = r"(\+7|8)\s*\(?(495)\)?\s*\-?(\d{3})\-?\s*(\d{2})\-?\s*(\d{2})\s*\(?([а-яА-Я.]+)?\s*(\d+)?\)?"
    pattern_sub = r"+7(\2)\3-\4-\5 \6\7"
    list_phone = []
    for i in contacts_list:
        phone_number = re.findall(pattern, ",".join(list(i)))
        if len(phone_number) != 0:
            phone = " ".join(list(phone_number[0]))
            res = re.sub(pattern, pattern_sub, phone)
            list_phone.append(res.rstrip())
        else:
            list_phone.append("")
    list_phone.pop(0)
    return(list_phone)

def organization(contacts_list):
        list_organization = []
        list_position = []
        for i in contacts_list:
            list_organization.append(i[3])
            list_position.append(i[4])
        list_organization.pop(0)
        list_position.pop(0)
        return(list_organization, list_position)

def union_date(phonebook):
    dict_phonebook = {}
    for i in phonebook:
        if i[0] not in dict_phonebook:
            dict_phonebook[i[0]] = list(i[1:])
        else:
            list_info = []
            for j in range(len(dict_phonebook.get(i[0]))):
                info = dict_phonebook.get(i[0])[j]
                if info == "":
                    list_info.append(i[j+1])
                else:
                    list_info.append(info)
            dict_phonebook[i[0]] = list_info
    phonebook = [[k, v] for k, v in dict_phonebook.items()]
    list_phonebook = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]
    for i in phonebook:
        list_1 = []
        list_1.append(i[0])
        for j in (i[1]):
            list_1.append(j)
        list_phonebook.append(list_1)
    return(list_phonebook)


## 2. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
def write_phonebook(list_phonebook):
    with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(list_phonebook)

if __name__ == '__main__':
    contacts_list = read_phonebook()
    phone = search_and_sub_phone(contacts_list)
    lastname, firstname, surname = search_full_name(contacts_list)
    email = search_email(contacts_list)
    org, pos = organization(contacts_list)
    res = zip(lastname, firstname, surname, org, pos, phone, email)
    phonebook = list(res)
    list_phonebook = union_date(phonebook)
    write_phonebook(list_phonebook)