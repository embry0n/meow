## Цель проекта

Создать приложение, которое:

- ✅ Хранит ваши пароли в одном месте
    
- ✅ Генерирует безопасные пароли
    
- ✅ Показывает список всех сохраненных записей
    
- ✅ Позволяет просматривать и удалять записи
    

## Структура нашего приложения

### Базовый шаблон - наша отправная точка

~~~python

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window

# Настраиваем внешний вид окна
Window.clearcolor = (0.05, 0.05, 0.05, 1)  # Темный фон
Window.size = (400, 600)  # Удобный размер для телефона

class PasswordManagerApp(App):
    def __init__(self):
        super().__init__()
        self.entries = []  # Здесь будем хранить наши пароли
        self.data_file = "passwords.json"  # Файл для сохранения данных
        self.load_data()  # Загружаем данные при запуске

    def build(self):
        # TODO: Создать интерфейс приложения
        # - Добавить заголовок
        # - Создать форму для ввода данных
        # - Добавить кнопки управления
        # - Создать список для отображения записей
        pass

    # Здесь будут все наши методы...
~~~
**Основные моменты:**

- `__init__` - это конструктор, он запускается при создании приложения
    
- `self.entries` - наш "список паролей", пока просто пустой список
    
- `self.data_file` - имя файла, где будем хранить данные
    
- `build()` - главный метод, который создает интерфейс
    

---

## Шаг 1: Создаем интерфейс (метод build)

### Что мы хотим получить:

~~~text

[ ЗАГОЛОВОК ]
[Поле Сервис] [Поле Логин] [Поле Пароль]
[   Кнопка Добавить   ] [Кнопка Генерировать]
[      Всего записей: 0     ]
[ Список сохраненных записей ]
~~~
### Реализация:

~~~python

def build(self):
    # Главный контейнер - все будет внутри него
    main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
    
    # 🎨 Заголовок приложения
    title = Label(
        text='🔐 Менеджер паролей',
        size_hint_y=None,  # Фиксированная высота
        height=50,         # Высота 50 пикселей
        font_size='22sp',  # Размер шрифта
        bold=True          # Жирный шрифт
    )
    main_layout.add_widget(title)
    
    # 📝 Форма для ввода данных (3 поля)
    input_layout = GridLayout(cols=2, size_hint_y=None, height=140, spacing=8)
    
    # Поле "Сервис"
    input_layout.add_widget(Label(text='Сервис:'))
    self.service_input = TextInput(
        multiline=False,
        hint_text='Например: Google',
        size_hint_y=None,
        height=40
    )
    input_layout.add_widget(self.service_input)
    
    # Поле "Логин"  
    input_layout.add_widget(Label(text='Логин:'))
    self.login_input = TextInput(
        multiline=False,
        hint_text='Email или логин',
        size_hint_y=None,
        height=40
    )
    input_layout.add_widget(self.login_input)
    
    # Поле "Пароль" (скрываем символы)
    input_layout.add_widget(Label(text='Пароль:'))
    self.password_input = TextInput(
        multiline=False,
        hint_text='Введите пароль',
        password=True,  # 🔒 Скрываем вводимые символы
        size_hint_y=None,
        height=40
    )
    input_layout.add_widget(self.password_input)
    
    main_layout.add_widget(input_layout)
    
    # 🎛️ Панель кнопок
    buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
    
    # Кнопка "Добавить"
    add_btn = Button(
        text='➕ Добавить',
        background_color=(0.2, 0.7, 0.3, 1)  # Зеленый цвет
    )
    add_btn.bind(on_press=self.add_password_entry)  # ⚡ Привязываем действие
    buttons_layout.add_widget(add_btn)
    
    # Кнопка "Сгенерировать"
    generate_btn = Button(
        text='🎲 Сгенерировать', 
        background_color=(0.2, 0.5, 0.8, 1)  # Синий цвет
    )
    generate_btn.bind(on_press=self.generate_password)
    buttons_layout.add_widget(generate_btn)
    
    main_layout.add_widget(buttons_layout)
    
    # ℹ️ Информация о количестве записей
    self.info_label = Label(
        text=f'Всего записей: {len(self.entries)}',
        size_hint_y=None,
        height=35,
        bold=True,
        font_size='16sp'
    )
    main_layout.add_widget(self.info_label)
    
    # 📜 Список записей с прокруткой
    scroll = ScrollView()  # Позволяет прокручивать длинные списки
    
    self.entries_list = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
    # Магия автоматической высоты:
    self.entries_list.bind(minimum_height=self.entries_list.setter('height'))
    
    scroll.add_widget(self.entries_list)
    main_layout.add_widget(scroll)
    
    return main_layout
~~~
**💡 Важные моменты:**

- `size_hint_y=None` + `height=...` - фиксируем высоту виджета
    
- `bind()` - "привязывает" функцию к нажатию кнопки
    
- `ScrollView` - как окно, через которое мы смотрим на длинный список
    
- `minimum_height` - волшебное свойство для автоматической высоты
    

---

## Шаг 2: Сохранение и загрузка данных

### Зачем это нужно?

Чтобы ваши пароли не пропадали после закрытия приложения!

~~~python

import json
import os
from datetime import datetime

def load_data(self):
    """Загружаем данные из файла при запуске"""
    try:
        # Проверяем, существует ли файл
        if os.path.exists(self.data_file):
            # Открываем файл для чтения
            with open(self.data_file, 'r', encoding='utf-8') as f:
                # Преобразуем JSON обратно в Python список
                self.entries = json.load(f)
    except Exception as e:
        # Если что-то пошло не так, начинаем с пустого списка
        print(f"Ошибка загрузки: {e}")
        self.entries = []

def save_data(self):
    """Сохраняем данные в файл"""
    try:
        # Открываем файл для записи
        with open(self.data_file, 'w', encoding='utf-8') as f:
            # Преобразуем список в JSON и сохраняем
            json.dump(self.entries, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

**🎓 Объяснение:**

- `json` - формат для хранения данных (как текстовый файл с структурой)
    
- `try-except` - ловим ошибки, чтобы приложение не "падало"
    
- `with open()` - автоматически закрывает файл после работы
    
- `ensure_ascii=False` - правильно сохраняет русские буквы
    

---
~~~
## Шаг 3: Добавление новой записи

~~~python

def add_password_entry(self, instance):
    """Добавляем новую запись о пароле"""
    
    # 📥 Получаем данные из полей ввода
    service = self.service_input.text.strip()    # Убираем лишние пробелы
    login = self.login_input.text.strip()
    password = self.password_input.text.strip()
    
    # ✅ Проверяем, что все поля заполнены
    if not service or not login or not password:
        self.show_message("Ошибка", "Заполните все поля!")
        return  # Если что-то не заполнено - выходим из функции
    
    # 🆕 Создаем новую запись
    new_entry = {
        'id': len(self.entries) + 1,           # Простой способ создать ID
        'service': service,                    # Название сервиса
        'login': login,                        # Логин или email  
        'password': password,                  # Пароль
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Дата создания
    }
    
    # 💾 Сохраняем запись
    self.entries.append(new_entry)  # Добавляем в список
    self.save_data()                # Сохраняем в файл
    
    # 🧹 Очищаем поля ввода
    self.service_input.text = ''
    self.login_input.text = ''
    self.password_input.text = ''
    
    # 🔄 Обновляем интерфейс
    self.update_entries_list()
~~~
**Что происходит:**

1. Берем текст из полей ввода
    
2. Проверяем, что ничего не пустое
    
3. Создаем "словарь" с информацией о пароле
    
4. Сохраняем в список и в файл
    
5. Очищаем форму для нового ввода
    
6. Обновляем список на экране
    

---

## Шаг 4: Генератор паролей

~~~python

import random
import string

def generate_password(self, instance):
    """Генерируем случайный безопасный пароль"""
    
    # 📏 Длина пароля (12 символов - хороший баланс)
    length = 12
    
    # 🔤 Какие символы можно использовать:
    # - Буквы (большие и маленькие): string.ascii_letters
    # - Цифры: string.digits  
    # - Спецсимволы: !@#$%^&*
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    
    # 🎰 Генерируем пароль:
    # - random.choice(characters) - берем случайный символ
    # - for _ in range(length) - повторяем 12 раз
    # - ''.join() - склеиваем все символы в одну строку
    password = ''.join(random.choice(characters) for _ in range(length))
    
    # 📝 Вставляем пароль в поле ввода
    self.password_input.text = password
~~~
**Почему это безопасно:**

- 12 символов = миллионы комбинаций
    
- Используем разные типы символов
    
- `random.choice` дает случайный результат
    

---

## Шаг 5: Показ списка записей

~~~python

def update_entries_list(self):
    """Обновляем список записей на экране"""
    
    # 🧹 Очищаем старый список
    self.entries_list.clear_widgets()
    
    # 🔄 Для каждой записи создаем строку в списке
    for entry in self.entries:
        # Создаем контейнер для одной записи
        entry_layout = BoxLayout(size_hint_y=None, height=40, spacing=5)
        
        # 🏷️ Название сервиса
        service_label = Label(
            text=entry['service'],
            size_hint_x=0.4,      # Занимает 40% ширины
            text_size=(None, None),  # Позволяет переносить текст
            halign='left'         # Выравнивание по левому краю
        )
        entry_layout.add_widget(service_label)
        
        # 👤 Логин
        login_label = Label(
            text=entry['login'], 
            size_hint_x=0.4,
            text_size=(None, None),
            halign='left'
        )
        entry_layout.add_widget(login_label)
        
        # 👁️ Кнопка просмотра
        view_btn = Button(
            text='👁',
            size_hint_x=0.2,      # Занимает 20% ширины
            background_color=(0.3, 0.3, 0.3, 1)  # Темно-серый
        )
        # Привязываем просмотр деталей этой записи
        view_btn.bind(on_press=lambda x, eid=entry['id']: self.show_entry_details(eid))
        entry_layout.add_widget(view_btn)
        
        # ➕ Добавляем запись в общий список
        self.entries_list.add_widget(entry_layout)
    
    # 🔢 Обновляем счетчик записей
    self.info_label.text = f'Всего записей: {len(self.entries)}'
~~~
**Как это выглядит:**

~~~text

[ Google    | user@gmail.com | 👁 ]
[ YouTube   | mychannel      | 👁 ]  
[ Facebook  | myprofile      | 👁 ]
~~~
---

## Шаг 6: Просмотр деталей записи

~~~python

def show_entry_details(self, entry_id):
    """Показываем всплывающее окно с деталями записи"""
    
    # 🔍 Ищем запись по ID
    entry = next((e for e in self.entries if e['id'] == entry_id), None)
    if not entry:
        return  # Если не нашли - выходим
    
    # 🪟 Создаем содержимое всплывающего окна
    content = BoxLayout(orientation='vertical', spacing=10, padding=10)
    
    # 📄 Показываем информацию о записи
    content.add_widget(Label(text=f"Сервис: {entry['service']}"))
    content.add_widget(Label(text=f"Логин: {entry['login']}")) 
    content.add_widget(Label(text=f"Пароль: {entry['password']}"))
    
    # 🎛️ Кнопки управления
    buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=5)
    
    # 🗑️ Кнопка удаления
    delete_btn = Button(text='Удалить')
    delete_btn.bind(on_press=lambda x: self.delete_entry(entry_id))
    buttons_layout.add_widget(delete_btn)
    
    # ❌ Кнопка закрытия
    close_btn = Button(text='Закрыть') 
    close_btn.bind(on_press=lambda x: popup.dismiss())
    buttons_layout.add_widget(close_btn)
    
    content.add_widget(buttons_layout)
    
    # 🪟 Создаем и показываем всплывающее окно
    popup = Popup(title='Детали записи', content=content, size_hint=(0.8, 0.5))
    popup.open()
~~~
**Что нового:**

- `Popup` - всплывающее окно поверх основного
    
- `next()` + генератор - красивый способ найти элемент в списке
    
- `dismiss()` - закрывает popup
    

---

## Шаг 7: Удаление записей

~~~python

def delete_entry(self, entry_id):
    """Удаляем запись из списка"""
    
    # 🧹 Фильтруем список, оставляя все кроме удаляемой записи
    self.entries = [entry for entry in self.entries if entry['id'] != entry_id]
    
    # 💾 Сохраняем изменения
    self.save_data()
    
    # 🔄 Обновляем интерфейс
    self.update_entries_list()
    
    # ✅ Показываем сообщение об успехе
    self.show_message("Успех", "Запись удалена!")
~~~
**🎯 Просто и эффективно:**

- Создаем новый список без удаляемого элемента
    
- Сохраняем и обновляем интерфейс
    
- Уведомляем пользователя
    

---

## Шаг 8: Показ сообщений

~~~python

def show_message(self, title, message):
    """Показываем всплывающее сообщение"""
    
    # 📦 Создаем содержимое сообщения
    content = BoxLayout(orientation='vertical', spacing=10, padding=10)
    content.add_widget(Label(text=message))  # Текст сообщения
    
    # 👌 Кнопка OK
    ok_btn = Button(text='OK', size_hint_y=None, height=40)
    content.add_widget(ok_btn)
    
    # 🪟 Создаем popup
    popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
    
    # ⚡ Привязываем закрытие окна к кнопке OK
    ok_btn.bind(on_press=popup.dismiss)
    
    # 🔓 Показываем сообщение
    popup.open()
~~~
---

## Запуск приложения

~~~python

if __name__ == '__main__':
    PasswordManagerApp().run()
~~~

# Желаемый результат
~~~python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
import random
import string
import json
import os
from datetime import datetime

Window.clearcolor = (0.05, 0.05, 0.05, 1)
Window.size = (400, 600)

class PasswordManagerApp(App):
    def __init__(self):
        super().__init__()
        self.entries = []
        self.data_file = "passwords.json"
        self.load_data()

    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        title = Label(
            text='Менеджер паролей',
            size_hint_y=None,
            height=50,
            font_size='22sp',
            bold=True
        )
        main_layout.add_widget(title)
        
        input_layout = GridLayout(cols=2, size_hint_y=None, height=140, spacing=8)
        
        input_layout.add_widget(Label(text='Сервис:'))
        self.service_input = TextInput(
            multiline=False,
            hint_text='Например: Google',
            size_hint_y=None,
            height=40
        )
        input_layout.add_widget(self.service_input)
        
        input_layout.add_widget(Label(text='Логин:'))
        self.login_input = TextInput(
            multiline=False,
            hint_text='Email или логин',
            size_hint_y=None,
            height=40
        )
        input_layout.add_widget(self.login_input)
        
        input_layout.add_widget(Label(text='Пароль:'))
        self.password_input = TextInput(
            multiline=False,
            hint_text='Введите пароль',
            password=True,
            size_hint_y=None,
            height=40
        )
        input_layout.add_widget(self.password_input)
        
        main_layout.add_widget(input_layout)
        
        buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        add_btn = Button(
            text='Добавить',
            background_color=(0.2, 0.7, 0.3, 1)
        )
        add_btn.bind(on_press=self.add_password_entry)
        buttons_layout.add_widget(add_btn)
        
        generate_btn = Button(
            text='Сгенерировать',
            background_color=(0.2, 0.5, 0.8, 1)
        )
        generate_btn.bind(on_press=self.generate_password)
        buttons_layout.add_widget(generate_btn)
        
        main_layout.add_widget(buttons_layout)
        
        self.info_label = Label(
            text=f'Всего записей: {len(self.entries)}',
            size_hint_y=None,
            height=35,
            bold=True,
            font_size='16sp'
        )
        main_layout.add_widget(self.info_label)
        
        scroll = ScrollView()
        self.entries_list = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.entries_list.bind(minimum_height=self.entries_list.setter('height'))
        scroll.add_widget(self.entries_list)
        main_layout.add_widget(scroll)
        
        self.update_entries_list()
        return main_layout

    def add_password_entry(self, instance):
        service = self.service_input.text.strip()
        login = self.login_input.text.strip()
        password = self.password_input.text.strip()
        
        if not service or not login or not password:
            self.show_message("Ошибка", "Заполните все поля!")
            return
        
        new_entry = {
            'id': len(self.entries) + 1,
            'service': service,
            'login': login,
            'password': password,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.entries.append(new_entry)
        self.save_data()
        self.service_input.text = ''
        self.login_input.text = ''
        self.password_input.text = ''
        self.update_entries_list()

    def generate_password(self, instance):
        length = 12
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_input.text = password

    def update_entries_list(self):
        
        self.entries_list.clear_widgets()
        
        for entry in self.entries:
            entry_layout = BoxLayout(size_hint_y=None, height=40, spacing=5)
            
            service_label = Label(
                text=entry['service'],
                size_hint_x=0.4,
                text_size=(None, None),
                halign='left'
            )
            entry_layout.add_widget(service_label)
            
            login_label = Label(
                text=entry['login'],
                size_hint_x=0.4,
                text_size=(None, None),
                halign='left'
            )
            entry_layout.add_widget(login_label)
            
            view_btn = Button(
                text='Просмотр',
                size_hint_x=0.2,
                background_color=(0.3, 0.3, 0.3, 1)
            )
            view_btn.bind(on_press=lambda x, eid=entry['id']: self.show_entry_details(eid))
            entry_layout.add_widget(view_btn)
            
            self.entries_list.add_widget(entry_layout)
        
        self.info_label.text = f'Всего записей: {len(self.entries)}'

    def show_entry_details(self, entry_id):
        entry = next((e for e in self.entries if e['id'] == entry_id), None)
        if not entry:
            return
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f"Сервис: {entry['service']}"))
        content.add_widget(Label(text=f"Логин: {entry['login']}"))
        content.add_widget(Label(text=f"Пароль: {entry['password']}"))
        
        buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=5)
        
        delete_btn = Button(text='Удалить')
        delete_btn.bind(on_press=lambda x: self.delete_entry(entry_id))
        buttons_layout.add_widget(delete_btn)
        
        close_btn = Button(text='Закрыть')
        close_btn.bind(on_press=lambda x: popup.dismiss())
        buttons_layout.add_widget(close_btn)
        
        content.add_widget(buttons_layout)
        
        popup = Popup(title='Детали записи', content=content, size_hint=(0.8, 0.5))
        popup.open()

    def delete_entry(self, entry_id):
        self.entries = [entry for entry in self.entries if entry['id'] != entry_id]
        self.save_data()
        self.update_entries_list()
        self.show_message("Успех", "Запись удалена!")

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.entries = json.load(f)
        except:
            self.entries = []

    def save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=2)
        except:
            pass

    def show_message(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=message))
        
        ok_btn = Button(text='OK', size_hint_y=None, height=40)
        content.add_widget(ok_btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    PasswordManagerApp().run()
~~~
