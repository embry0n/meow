
## 1. Введение в Kivy

### Что такое Kivy?
- **Kivy** - это фреймворк для создания кроссплатформенных приложений на Python
- Работает на Windows, Mac, Linux, Android, iOS
- Использует собственный язык разметки (.kv файлы) или чистый Python

### Основные понятия:
```python
# Базовая структура Kivy приложения
from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        return Label(text='Привет, мир!')

MyApp().run()
```

### Установка Kivy:
```bash
pip install kivy
```



## 2. Основные виджеты и компоновка 

### 2.1 Базовые виджеты

#### Label - для отображения текста
```python
Label(
    text='Привет, мир!',
    font_size='20sp',      # sp - масштабируемые пиксели
    color=(1, 0, 0, 1),    # Цвет (R, G, B, A)
    bold=True,
    size_hint_y=None,      # Фиксированная высота
    height=50
)
```

#### Button - кликабельные кнопки
```python
Button(
    text='Нажми меня',
    background_color=(0.2, 0.6, 0.8, 1),  # Синий цвет
    size_hint_y=None,
    height=40
)
```

#### TextInput - поля ввода
```python
TextInput(
    hint_text='Введите текст...',
    multiline=False,        # Однострочное поле
    size_hint_y=None,
    height=40
)
```

#### Spinner - выпадающий список
```python
Spinner(
    text='Выберите вариант',
    values=['Вариант 1', 'Вариант 2', 'Вариант 3'],
    size_hint_y=None,
    height=40
)
```

### 2.2 Компоновщики (Layouts)

#### BoxLayout - линейное расположение
```python
# Вертикальное расположение
BoxLayout(
    orientation='vertical',
    padding=10,        # Отступы внутри
    spacing=5          # Расстояние между элементами
)

# Горизонтальное расположение  
BoxLayout(orientation='horizontal')
```

#### GridLayout - сетка
```python
GridLayout(
    cols=2,           # 2 колонки
    rows=3,           # 3 строки
    spacing=10,
    size_hint_y=None,
    height=200
)
```

#### ScrollView - прокручиваемая область
```python
ScrollView():
    BoxLayout(
        orientation='vertical',
        size_hint_y=None
    )
```

### 2.3 Размеры и позиционирование

#### size_hint - как виджет растягивается:
- `size_hint=(1, 1)` - растягивается на всё доступное пространство
- `size_hint=(0.5, None)` - ширина 50%, высота фиксированная
- `size_hint_y=None` - фиксированная высота (требует указания height)

#### Пример:
```python
Label(
    text='Фиксированная высота',
    size_hint_y=None,    # Не растягивается по вертикали
    height=50            # Фиксированная высота 50px
)

Label(
    text='Растягивается',
    size_hint=(1, 1)     # Растягивается на всё пространство
)
```



## 3. Практическая работа

### Задание 1: Создайте простой интерфейс с приветствием

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class SimpleApp(App):
    def build(self):
        # Главный контейнер
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=10
        )
        
        # Заголовок
        title = Label(
            text='Добро пожаловать!',
            font_size='24sp',
            size_hint_y=None,
            height=60
        )
        
        # Кнопка
        btn = Button(
            text='Нажми меня',
            size_hint_y=None,
            height=50
        )
        
        layout.add_widget(title)
        layout.add_widget(btn)
        
        return layout

SimpleApp().run()
```

### Задание 2: Добавьте форму ввода

```python
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

class FormApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Заголовок
        main_layout.add_widget(Label(
            text='Регистрация',
            font_size='20sp',
            size_hint_y=None,
            height=50
        ))
        
        # Форма ввода
        form = GridLayout(cols=2, size_hint_y=None, height=120, spacing=10)
        
        form.add_widget(Label(text='Имя:'))
        name_input = TextInput(multiline=False)
        form.add_widget(name_input)
        
        form.add_widget(Label(text='Email:'))
        email_input = TextInput(multiline=False)
        form.add_widget(email_input)
        
        main_layout.add_widget(form)
        
        # Кнопка
        main_layout.add_widget(Button(
            text='Зарегистрироваться',
            size_hint_y=None,
            height=50
        ))
        
        return main_layout

FormApp().run()
```



## 4. Создание интерфейса нашего приложения

### Полный код интерфейса финансового приложения:

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.core.window import Window

# Настройка окна
Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Светло-серый фон
Window.size = (400, 600)  # Размер окна

class FinanceApp(App):
    def build(self):
        # === ГЛАВНЫЙ КОНТЕЙНЕР ===
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=15, 
            spacing=10
        )
        
        # === ЗАГОЛОВОК ===
        title = Label(
            text='💸 Учет расходов',
            size_hint_y=None,
            height=50,
            font_size='22sp',
            bold=True
        )
        main_layout.add_widget(title)
        
        # === ФОРМА ДЛЯ ВВОДА РАСХОДОВ ===
        input_layout = GridLayout(
            cols=2, 
            size_hint_y=None, 
            height=140, 
            spacing=8
        )
        
        # Поле для суммы
        input_layout.add_widget(Label(text='Сумма (руб):'))
        self.amount_input = TextInput(
            multiline=False,
            input_filter='float',  # Только числа
            hint_text='Например: 150.50',
            size_hint_y=None,
            height=40
        )
        input_layout.add_widget(self.amount_input)
        
        # Выбор категории
        input_layout.add_widget(Label(text='Категория:'))
        self.category_spinner = Spinner(
            text='Транспорт',
            values=['Транспорт', 'Продукты', 'Развлечения', 'Здоровье', 'Одежда', 'Другое'],
            size_hint_y=None,
            height=40
        )
        input_layout.add_widget(self.category_spinner)
        
        # Поле для описания
        input_layout.add_widget(Label(text='Описание:'))
        self.desc_input = TextInput(
            multiline=False,
            hint_text='Необязательно',
            size_hint_y=None,
            height=40
        )
        input_layout.add_widget(self.desc_input)
        
        main_layout.add_widget(input_layout)
        
        # === ПАНЕЛЬ КНОПОК ===
        buttons_layout = BoxLayout(
            size_hint_y=None, 
            height=50, 
            spacing=10
        )
        
        # Кнопка добавления расхода
        add_btn = Button(
            text='➕ Добавить',
            background_color=(0.2, 0.7, 0.3, 1)  # Зеленый
        )
        buttons_layout.add_widget(add_btn)
        
        # Кнопка просмотра статистики
        stats_btn = Button(
            text='📊 Статистика', 
            background_color=(0.2, 0.5, 0.8, 1)  # Синий
        )
        buttons_layout.add_widget(stats_btn)
        
        main_layout.add_widget(buttons_layout)
        
        # === ОБЩАЯ СУММА РАСХОДОВ ===
        self.total_label = Label(
            text='Всего потрачено: 0 руб',
            size_hint_y=None,
            height=35,
            bold=True,
            font_size='16sp'
        )
        main_layout.add_widget(self.total_label)
        
        # === СПИСОК РАСХОДОВ ===
        scroll = ScrollView()
        
        # Контейнер для списка расходов
        self.expenses_list = BoxLayout(
            orientation='vertical', 
            spacing=5, 
            size_hint_y=None
        )
        # Важно: привязываем минимальную высоту к фактической высоте
        self.expenses_list.bind(minimum_height=self.expenses_list.setter('height'))
        
        scroll.add_widget(self.expenses_list)
        main_layout.add_widget(scroll)
        
        return main_layout

# Запуск приложения
if __name__ == '__main__':
    FinanceApp().run()
```

### Разбор ключевых моментов:

1. **Иерархия виджетов:**
   ```
   BoxLayout (вертикальный)
   ├── Label (заголовок)
   ├── GridLayout (форма ввода)
   │   ├── Label + TextInput (сумма)
   │   ├── Label + Spinner (категория)  
   │   └── Label + TextInput (описание)
   ├── BoxLayout (кнопки)
   │   ├── Button (добавить)
   │   └── Button (статистика)
   ├── Label (общая сумма)
   └── ScrollView
       └── BoxLayout (список расходов)
   ```

2. **Сохраняем ссылки на виджеты:**
   - `self.amount_input`, `self.category_spinner`, `self.desc_input` - чтобы потом получить из них данные
   - `self.expenses_list` - чтобы динамически добавлять расходы

3. **Особенности ScrollView:**
   - Внутренний контейнер должен иметь `size_hint_y=None`
   - Нужно привязать `minimum_height` к `height`



## 5. Итоги и домашнее задание

### Что мы узнали:
- Основы фреймворка Kivy
- Основные виджеты: Label, Button, TextInput, Spinner
- Компоновщики: BoxLayout, GridLayout, ScrollView
- Управление размерами через size_hint и height/width


### Полезные ресурсы:
- [Официальная документация Kivy](https://kivy.org/doc/stable/)
- [Kivy Tutorial на русском](https://kivy-russia.github.io/ru/)
- [Примеры приложений на Kivy](https://github.com/kivy/kivy/tree/master/examples)
