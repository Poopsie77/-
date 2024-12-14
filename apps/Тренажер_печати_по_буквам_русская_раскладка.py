import tkinter as tk
from time import perf_counter
from random import choice
from PIL import Image, ImageTk
import os


# Список текстов для разных уровней сложности и языков
texts = {
    'йцулдя': {
        'ru': [
            'йцулдяцулдяяулййцулйцулдядяцулдяйцулдяйцйцйцуйцуйцулдялдялдяулдййцулдяцулдяяулййцуулдяйцуйцулдялдядя',
            'йцулйццулдяйцйцйцуйцуулдядяцулдяйцулдяйцйцйцуйцуйцулййцуулдяйцуйцулдулдялдялдцулдяйцййцуулдяйцуйцулд',
        ]
    },
    'смзхыб': {
        'ru': [
            'смзхыбмзхысмзхыбсмзхыбсмзхысмзхыбсмзхыссмзхыбмзхысмзхыбсмзхыбсмзхысмзхыбсмсбмзхыбсмзыбзхыбсмзхыбсмзх',
            'ысмзхыбсмзхмзыссмзхыбмбмзхысмзхыбсмзхыбсмзхысмзхыбсмзхыссмзхыбмзхысмзхыбсмзхыхызхысмзхыбсмзхыбсмзхыс',
        ]
    },
    'фызшпр': {
        'ru': [
            'зшпрфыфызшпрзфызшпрфыфызшпрзшпрфыфызшпрзфызшзшпрфыфызшпрзфызшпрпршпрфыфызшпрзфызшзшпрфыфызшпырзфыфзп',
            'ыфызшрфыфызшпрзфызшзшпрфыфызшпрзфызшпрзфызшпрзфызшзшпрфыфызшпрфыфызшпрзшпрфыфызшпрзфызшзшпрфыфыфызщф',
        ]
    },
    'йфякехж': {
        'ru': [
            'йфякехжфякехжехжйфяйфякехжйфякйфякехжйфякехжфякехжехжйфяйфякехжкехжйфякехжйфякехжфякехжехжйфяйфякехж',
            'йфякехжфякехжехжйфяйфякехжфякехжфякейфякехжфякехжехжйфяйфякехфякехжфякехжфякежхжехжйфяйфякехжфяжфяке',
        ]
    },
    'клйзсь': {
        'ru': [
            'кклйзсьлйклйззськсьлйклйзсьлйзськлйклйзсьзсклйзсьлйзськлйкьзьлйклйклйзсьлйклйзсьлйзськлйклйзсьзсьзсь',
            'лйклйлйклйззськсьлйклйзсьлйзськлйклйзсьзсклйзсьлйззсьлйклйззськсьлйклйзсьлйзськлйклйзсськлйклййзсьлй'
        ]
    }
}


try:
    from PIL import ImageTk, Image
except ImportError:
    pass

class Typingtest(tk.Tk):
    """
     Класс для создания приложения теста на скорость печати.

     Атрибуты:
         start_time (float): Время начала теста.
         end_time (float): Время завершения теста.
         total_characters (int): Общее количество символов в тексте.
         correct_characters (int): Количество правильно введённых символов.
         wpm (int): Скорость печати в словах в минуту.
         accuracy (int): Точность ввода в процентах.
         level (str): Уровень сложности теста.
         language (str): Язык текста для теста.
         en_label (tk.Label): Метка для отображения картинки.
         current_letter_index (int): Индекс текущего символа.
         level_var (tk.StringVar): Переменная для выбора уровня сложности.
         language_var (tk.StringVar): Переменная для выбора языка.
         label_text (tk.Text): Виджет для отображения текста задания.
         entry (tk.Entry): Поле ввода для ответа пользователя.
         start_button (tk.Button): Кнопка для начала теста.
         stats_frame (tk.Frame): Фрейм для отображения статистики.
         keyboard_frame (tk.Frame): Фрейм для отображения виртуальной клавиатуры.
    """

    def __init__(self):
        """
        Инициализация главного окна приложения.
        Настройка элементов интерфейса и начальных значений.
                """
        super().__init__()

        self.title("Тест скорости печати")
        self.geometry("1200x600")
        # Устанавливаем синий фон для всего окна
        self.configure(bg='#E6F7FF')

        # Переменные для отслеживания статистики
        self.start_time = None
        self.end_time = None
        self.total_characters = 0
        self.correct_characters = 0
        self.wpm = 0
        self.accuracy = 0

        # Текущий уровень сложности и язык
        self.level = 'йцулдя'
        self.language = 'ru'

        self.ru_label = tk.Label(self, bg="#E6F7FF")
        self.ru_label.pack(padx=10, pady=70)

        base_dir = os.path.dirname(os.path.abspath(__file__))  # Путь до текущей директории (где находится ваш скрипт)
        image_path = os.path.join(base_dir, '..', 'images', 'fingers.jpg')  # Путь к изображению
        # Путь к картинке
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        self.ru_label['image'] = photo
        self.ru_label.image = photo
        self.ru_label.pack(side=tk.BOTTOM, fill=tk.BOTH)

        # Индекс текущей буквы в тексте
        self.current_letter_index = 0

        # Меню для выбора уровня сложности и языка
        menu_frame = tk.Frame(self,bg='#E6F7FF')
        level_label = tk.Label(menu_frame, text="Уровень сложности:",bg='#E6F7FF')
        level_label.grid(row=0, column=0, padx=5, pady=5)
        self.level_var = tk.StringVar(value='йцулдя')
        level_options = ['йцулдя', 'смзхыб', 'фызшпр','йфякехж','клйзсь']
        level_menu = tk.OptionMenu(menu_frame, self.level_var, *level_options, command=self.change_level)
        level_menu.grid(row=0, column=1, padx=5, pady=5)

        language_label = tk.Label(menu_frame, text="Язык:",bg='#E6F7FF')
        language_label.grid(row=1, column=0, padx=5, pady=5)
        self.language_var = tk.StringVar(value='ru')
        language_options = ['ru']
        language_menu = tk.OptionMenu(menu_frame, self.language_var, *language_options, command=self.change_language)
        language_menu.grid(row=1, column=1, padx=5, pady=5)


        menu_frame.pack(side=tk.TOP, fill=tk.X)

        # Метка для отображения текста задания
        self.label_text = tk.Text(self, height=5, wrap=tk.WORD, font=("Arial", 18))
        self.label_text.tag_configure('green', foreground='green')
        self.label_text.tag_configure('red', foreground='red')
        self.label_text.pack(pady=10)



        # Поле ввода для ответа пользователя
        self.entry = tk.Entry(self, width=90)
        self.entry.bind("<KeyRelease>", self.on_key_release)
        self.entry.pack()

        # Кнопка для начала теста
        self.start_button = tk.Button(self, text="Начать тест", command=self.start_test)
        self.start_button.pack(pady=10)

        # Статистика
        self.stats_frame = tk.Frame(self)
        self.stats_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.stats_labels = []
        self.stats_frame.configure(bg="#E6F7FF")
        for i in range(4):
            label = tk.Label(self.stats_frame, anchor=tk.SW)
            label.grid(row=i, column=0, sticky=tk.SW)
            self.stats_frame.configure(bg="#E6F7FF")
            self.stats_labels.append(label)


        # Виртуальная клавиатура
        self.keyboard_frame = tk.Frame(self)
        self.keyboard_frame.pack(expand=True, fill=tk.BOTH)
        self.keyboard_frame.place(x=300, y=305)
        self.keyboard_frame.configure(bg="#E6F7FF")

        self.buttons = {}
        self.create_keyboard()

        self.update_text()



    # Русская раскладка
    def create_keyboard(self):
        """
        Создание виртуальной клавиатуры для теста.
        В зависимости от выбранного языка создаются кнопки для клавиш, а также назначаются их действия.
                """
        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()

        if self.language == 'ru':
            rows = [
                ["Ё", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=" "+", "Backspace ⌫"],
                ['Tab ⇥','',"Й", "Ц", "У", "К", "Е", "Н", "Г", "Ш", "Щ", "З", "Х", "Ъ",'\\','|', '/'],
                ["Caps Lock",'', '',"Ф", "Ы", "В", "А", "П", "Р", "О", "Л", "Д", "Ж", "Э", "↵ Enter"],
                ["Shift",'', "Я", "Ч", "С", "М", "И", "Т", "Ь", "Б", "Ю", ",", ".", "Shift ⇧"],
                ["Ctrl", "Win", "Alt", "Space", '','','', '',"Alt", "Win", "Ctrl", "←", "↑", "↓", "→"]
            ]

        for r, row in enumerate(rows):
            for c, char in enumerate(row):
                if char == "Tab ⇥":
                    btn = tk.Button(
                        self.keyboard_frame,
                        text="Tab ⇥",
                        command=lambda ch=char: self.add_char(ch),
                        font=("Arial", 14),
                        bg="#ffffff",
                        activebackground="#dcdcdc",
                        borderwidth=1,
                        relief="raised",
                        fg="#000000",
                        activeforeground="#000000",
                        width=10,  # Ширина пробела увеличена
                        height=2,
                        repeatdelay=200,
                        repeatinterval=50
                    )
                    btn.grid(row=r, column=c, columnspan=2,
                             sticky="nsew")
                elif char == "Shift":
                    btn = tk.Button(
                        self.keyboard_frame,
                        text="Shift",
                        command=lambda ch=char: self.add_char(ch),
                        font=("Arial", 14),
                        bg="#ffffff",
                        activebackground="#dcdcdc",
                        borderwidth=1,
                        relief="raised",
                        fg="#000000",
                        activeforeground="#000000",
                        width=10,  # Ширина пробела увеличена
                        height=2,
                        repeatdelay=200,
                        repeatinterval=50
                    )
                    btn.grid(row=r, column=c, columnspan=2,
                             sticky="nsew")
                elif char == "Shift ⇧":
                    btn = tk.Button(
                        self.keyboard_frame,
                        text="Shift ⇧",
                        command=lambda ch=char: self.add_char(ch),
                        font=("Arial", 14),
                        bg="#ffffff",
                        activebackground="#dcdcdc",
                        borderwidth=1,
                        relief="raised",
                        fg="#000000",
                        activeforeground="#000000",
                        width=15,  # Ширина пробела увеличена
                        height=2,
                        repeatdelay=200,
                        repeatinterval=50
                    )
                    btn.grid(row=r, column=c, columnspan=5,
                             sticky="nsew")
                elif char == "Space":
                    btn = tk.Button(
                        self.keyboard_frame,
                        text=" ",
                        command=lambda ch=char: self.add_char(ch),
                        font=("Arial", 14),
                        bg="#ffffff",
                        activebackground="#dcdcdc",
                        borderwidth=1,
                        relief="raised",
                        fg="#000000",
                        activeforeground="#000000",
                        width=15,  # Ширина пробела увеличена
                        height=2,
                        repeatdelay=200,
                        repeatinterval=50
                    )
                    btn.grid(row=r, column=c, columnspan=5,
                             sticky="nsew")  # Используем columnspan для объединения трех колонок
                elif char == '':
                    continue  # Пропуск пустых элементов

                elif char == "Backspace ⌫":
                    btn = tk.Button(
                        self.keyboard_frame,
                        text="Backspace ⌫",
                        command=lambda ch=char: self.add_char(ch),
                        font=("Arial", 14),
                        bg="#ffffff",
                        activebackground="#dcdcdc",
                        borderwidth=1,
                        relief="raised",
                        fg="#000000",
                        activeforeground="#000000",
                        width=15,  # Ширина пробела увеличена
                        height=2,
                        repeatdelay=200,
                        repeatinterval=50
                    )
                    btn.grid(row=r, column=c, columnspan=6,
                             sticky="nsew")
                elif char == "Caps Lock":
                    btn = tk.Button(
                        self.keyboard_frame,
                        text="Caps Lock",
                        command=lambda ch=char: self.add_char(ch),
                        font=("Arial", 14),
                        bg="#ffffff",
                        activebackground="#dcdcdc",
                        borderwidth=1,
                        relief="raised",
                        fg="#000000",
                        activeforeground="#000000",
                        width=15,  # Ширина пробела увеличена
                        height=2,
                        repeatdelay=200,
                        repeatinterval=50
                    )
                    btn.grid(row=r, column=c, columnspan=3,
                             sticky="nsew")
                elif char == "↵ Enter":
                    btn = tk.Button(
                        self.keyboard_frame,
                        text="↵ Enter",
                        command=lambda ch=char: self.add_char(ch),
                        font=("Arial", 14),
                        bg="#ffffff",
                        activebackground="#dcdcdc",
                        borderwidth=1,
                        relief="raised",
                        fg="#000000",
                        activeforeground="#000000",
                        width=15,  # Ширина пробела увеличена
                        height=2,
                        repeatdelay=200,
                        repeatinterval=50
                    )
                    btn.grid(row=r, column=c, columnspan=5,
                             sticky="nsew")

                else:
                    btn = tk.Button(
                        self.keyboard_frame,
                        text=char,
                        command=lambda ch=char: self.add_char(ch),
                        font=("Arial", 14),
                        bg="#ffffff",
                        activebackground="#dcdcdc",
                        borderwidth=1,
                        relief="raised",
                        fg="#000000",
                        activeforeground="#000000",
                        width=5,
                        height=2,
                        repeatdelay=200,
                        repeatinterval=50
                    )
                    btn.grid(row=r, column=c, ipadx=2, ipady=2)
                self.buttons[char] = btn


    def change_level(self, value):
        """
        Изменение уровня сложности.
        Args:
            level (str): Новый уровень сложности.
        """
        self.level = value
        self.update_text()


    def change_language(self, value):
        """
        Изменение языка.

        Args:
            language (str): Новый язык.
        """
        self.language = value
        self.create_keyboard()

        self.update_text()

    def update_text(self):
        """
        Обновление текста, который должен быть напечатан пользователем.
        Загрузка текста для текущего уровня сложности и языка, а также отображение его на экране.
        """
        texts_list = texts[self.level][self.language]
        self.current_text = choice(texts_list)
        self.label_text.delete('1.0', tk.END)
        self.label_text.insert(tk.END, self.current_text)

    def on_key_release(self, event):
        """
        Обработчик событий при нажатии клавиш. Проверка правильности введённых символов.

        Args:
            event (tk.Event): Событие нажатия клавиши.
        """
        current_input = self.entry.get().upper()
        original_text = self.current_text.upper()

        # Подсвечивание правильного и неправильного ввода
        for i, char in enumerate(current_input):
            if i < len(original_text) and char == original_text[i]:
                self.label_text.tag_add('green', f'1.{i}', f'1.{i+1}')
            else:
                self.label_text.tag_add('red', f'1.{i}', f'1.{i+1}')

        # Подсветка текущей буквы на клавиатуре
        if current_input:
            next_letter = original_text[len(current_input)]
            self.highlight_button(next_letter)

        # Завершение теста, если пользователь закончил ввод текста
        if current_input == original_text:
            self.end_test()

        # Обновление статистики в реальном времени
        self.update_stats()

    # Определите словарь цветов для каждой клавиши

    key_colors = {
        'Ё': '#FF0000',
        '1': '#FF0000',
        '2': '#FF0000',
        'Й': '#FF0000',
        'Ф': '#FF0000',
        'Я': '#FF0000',
        '8': '#FF0000',
        'Ш': '#FF0000',
        'Л': '#FF0000',
        'Б': '#FF0000',
        '3': '#FFFF00',
        'Ц': '#FFFF00',
        'Ы': '#FFFF00',
        'Ч': '#FFFF00',
        '9': '#FFFF00',
        'Щ': '#FFFF00',
        'Д': '#FFFF00',
        'Ю': '#FFFF00',
        '4': '#00FF00',
        'У': '#00FF00',
        'В': '#00FF00',
        'С': '#00FF00',
        '0': '#00FF00',
        '-': '#00FF00',
        '+': '#00FF00',
        'З': '#00FF00',
        'Х': '#00FF00',
        'Ъ': '#00FF00',
        'Ж': '#00FF00',
        'Э': '#00FF00',
        '?': '#00FF00',
        '.': '#FFFF00',
        ' ': '#8601AF',
        '7': '#8601AF',
        'Н': '#8601AF',
        'Г': '#8601AF',
        'Р': '#8601AF',
        'О': '#8601AF',
        'Т': '#8601AF',
        'Ь': '#8601AF',
        '5': '#40E0D0',
        '6': '#40E0D0',
        'К': '#40E0D0',
        'Е': '#40E0D0',
        'А': '#40E0D0',
        'П': '#40E0D0',
        'М': '#40E0D0',
        'И': '#40E0D0',

    }

    def highlight_button(self, char):
        if char == " ":
            self.buttons['Space'].configure(bg='#8601AF', fg='#000000', borderwidth=1, relief="sunken")
            self.buttons['Space'].highlight_button()
        for key, button in self.buttons.items():
            color = self.key_colors.get(key, "")  # используйте стандартный цвет, если нет специального
            if key == char:
                button.config(bg=color, relief="sunken")
            else:
                button.config(bg="#FFFFFF", relief="raised")

    def start_test(self):
        """
        Запуск теста.
        Сохранение времени старта и отображение первого символа.
        """
        self.start_time = perf_counter()
        self.entry.focus_set()
        self.entry.delete(0, tk.END)

    def end_test(self):
        """
        Завершение теста.
        Расчёт статистики: время, скорость, точность,
        правильные/неправильные символы,
        общее количество символов.
        """
        self.end_time = perf_counter()
        elapsed_time = self.end_time - self.start_time
        total_characters = len(self.current_text)
        correct_characters = sum([a == b for a, b in zip(self.entry.get(), self.current_text)])

        wpm = int(correct_characters / (elapsed_time / 60))
        accuracy = int((correct_characters / total_characters) * 100) if total_characters > 0 else 0

        self.stats_labels[0].config(text=f"Время: {elapsed_time:.2f} секунд")
        self.stats_labels[1].config(text=f"Скорость печати: {wpm} знаков/мин")
        self.stats_labels[2].config(text=f"Точность: {accuracy}%")
        self.stats_labels[3].config(text=f"Правильные символы: {correct_characters}")
        self.stats_labels[4].config(text=f"Неправильные символы: {total_characters - correct_characters}")
        self.stats_labels[5].config(text=f"Общее количество символов: {total_characters}")

    def add_char(self, char):
        """
        Добавление символа в поле ввода и обновление статистики.

        Эта функция добавляет новый символ в текущее состояние текста в поле ввода
        и вызывает обработчик событий для обновления состояния (проверки правильности ввода).

        Args:
            char (str): Символ, который необходимо добавить.
        """
        current_input = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, current_input + char)
        self.on_key_release(None)

    def delete_last(self):
        """
        Удаление последнего символа в поле ввода и обновление статистики.
        Эта функция удаляет последний введённый символ из поля ввода, если оно не пустое,
        и вызывает обработчик событий для обновления состояния.
        """
        current_input = self.entry.get()
        if current_input:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, current_input[:-1])
            self.on_key_release(None)

    def update_stats(self):
        """
        Обновление статистики по введённому тексту.
        Эта функция рассчитывает количество введённых символов,
        количество правильных и неправильных символов,
        а также вычисляет скорость печати и точность.
        Статистика обновляется на основе времени, прошедшего с начала теста,
        и текста, который был введён пользователем.
        """
        current_input = self.entry.get().lower()
        original_text = self.current_text.lower()

        total_characters = len(current_input)
        correct_characters = sum(a == b for a, b in zip(current_input, original_text) if b != '')
        incorrect_characters = total_characters - correct_characters

        if self.start_time is not None:
            elapsed_time = perf_counter() - self.start_time
            wpm = int(total_characters / (elapsed_time / 60)) if elapsed_time > 0 else 0
            accuracy = int((correct_characters / total_characters) * 100) if total_characters > 0 else 0
        else:
            elapsed_time = 0
            wpm = 0
            accuracy = 0

        self.stats_labels[0].config(text=f"Процент точности: {accuracy}%",bg='#E6F7FF')
        self.stats_labels[1].config(text=f"Скорость: {wpm} знаков/мин",bg='#E6F7FF')
        self.stats_labels[2].config(text=f"Общее количество введенных знаков: {total_characters}",bg='#E6F7FF')
        self.stats_labels[3].config(text=f"Количество правильных введённых знаков: {correct_characters}",bg='#E6F7FF')


if __name__ == "__main__":
    app = Typingtest()
    app.mainloop()