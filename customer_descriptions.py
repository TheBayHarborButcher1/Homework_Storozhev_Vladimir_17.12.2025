def load_csv_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def parse_customer_data(lines):
    if not lines:
        return []

    separator = ','
    headers_line = lines[0]

    # Заголовки из вашего файла
    if headers_line.startswith('name,device_type,browser,sex,age,bill,region'):
        # Ваш конкретный формат
        customers = []
        for i, line in enumerate(lines[1:], 1):
            if not line.strip():
                continue

            fields = line.split(',')
            if len(fields) >= 7:
                customer = {
                    'ФИО': fields[0].strip(),
                    'Устройство': fields[1].strip(),
                    'Браузер': fields[2].strip(),
                    'Пол': fields[3].strip(),
                    'Возраст': fields[4].strip(),
                    'Сумма': fields[5].strip(),
                    'Регион': fields[6].strip()
                }
                customers.append(customer)
        print(f"Успешно распарсено: {len(customers)} записей")
        return customers

    # Старый код для других форматов
    headers = [h.strip() for h in lines[0].split(separator)]

    field_mapping = {
        'name': 'ФИО', 'fio': 'ФИО', 'фио': 'ФИО',
        'device_type': 'Устройство', 'device': 'Устройство', 'устройство': 'Устройство',
        'browser': 'Браузер', 'браузер': 'Браузер',
        'sex': 'Пол', 'gender': 'Пол', 'пол': 'Пол',
        'age': 'Возраст', 'возраст': 'Возраст',
        'bill': 'Сумма', 'amount': 'Сумма', 'сумма': 'Сумма',
        'region': 'Регион', 'регион': 'Регион'
    }

    normalized_headers = []
    for header in headers:
        header_lower = header.lower()
        normalized_headers.append(field_mapping.get(header_lower, header))

    customers = []
    for i, line in enumerate(lines[1:], 1):
        if not line.strip():
            continue

        fields = line.split(separator)
        fields = [f.strip() for f in fields]

        if len(fields) != len(normalized_headers):
            continue

        customer = {}
        for j, header in enumerate(normalized_headers):
            customer[header] = fields[j]

        customers.append(customer)

    print(f"Успешно распарсено: {len(customers)} записей")
    return customers


def transform_gender(gender):
    if not gender:
        return {'display': 'неизвестного', 'verb': 'совершил(а)'}

    gender_lower = gender.lower()

    if 'female' in gender_lower or 'жен' in gender_lower or 'f' in gender_lower or 'ж' in gender_lower:
        return {'display': 'женского', 'verb': 'совершила'}
    elif 'male' in gender_lower or 'муж' in gender_lower or 'm' in gender_lower or 'м' in gender_lower:
        return {'display': 'мужского', 'verb': 'совершил'}
    else:
        return {'display': 'неизвестного', 'verb': 'совершил(а)'}


def transform_device(device):
    if not device:
        return 'устройства'

    device_lower = device.lower()

    if 'mobile' in device_lower:
        return 'мобильного'
    elif 'desktop' in device_lower:
        return 'компьютерного'
    elif 'laptop' in device_lower:
        return 'ноутбука'
    elif 'tablet' in device_lower:
        return 'планшетного'
    else:
        return 'устройства'


def create_description(customer):
    gender_info = transform_gender(customer.get('Пол', ''))
    device_display = transform_device(customer.get('Устройство', ''))

    description = (f"Пользователь {customer.get('ФИО', 'Неизвестно')} "
                   f"{gender_info['display']} пола, "
                   f"{customer.get('Возраст', 'неизвестно')} лет "
                   f"{gender_info['verb']} покупку на "
                   f"{customer.get('Сумма', '0')} у.е. с {device_display} браузера "
                   f"{customer.get('Браузер', 'неизвестно')}. "
                   f"Регион, из которого совершалась покупка: "
                   f"{customer.get('Регион', 'неизвестно')}.\n")

    return description


def save_descriptions_to_file(descriptions, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for desc in descriptions:
                file.write(desc)
        return True, len(descriptions)
    except Exception as e:
        return False, str(e)


def main():
    print("=" * 60)
    print("Программа для формирования описаний покупателей")
    print("=" * 60)

    input_file = 'web_clients_correct.csv'
    output_file = 'customers_descriptions.txt'

    print(f"\nЗагрузка данных из файла '{input_file}'...")
    lines = load_csv_file(input_file)

    if not lines:
        return

    print(f"Загружено строк: {len(lines)}")

    print(f"\nПарсинг данных...")
    customers = parse_customer_data(lines)

    if not customers:
        print("Не удалось распарсить данные")
        return

    print(f"\nСоздание описаний...")
    descriptions = []

    for customer in customers:
        description = create_description(customer)
        descriptions.append(description)

    print(f"\nСохранение описаний в файл '{output_file}'...")
    success, result = save_descriptions_to_file(descriptions, output_file)

    if success:
        print(f"Успешно сохранено {result} описаний")

        print(f"\nПримеры описаний:")
        print("-" * 60)

        for i in range(min(3, len(descriptions))):
            print(f"\nПример {i + 1}:")
            print(descriptions[i])

        print("-" * 60)
        print(f"\nВсего создано описаний: {len(descriptions)}")

    else:
        print(f"Ошибка сохранения: {result}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()