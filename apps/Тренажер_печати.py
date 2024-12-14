import tkinter as tk
from time import perf_counter
from random import choice
from PIL import Image, ImageTk

# Список текстов для разных уровней сложности и языков
texts = {
    'easy': {
        'ru': [
            'Это простой текст.',
            'Скорость печати очень важна.',
            'Попробуйте набрать этот текст быстро.'
        ],
        'en': [
            'This is an easy text.',
            'Typing speed is very important.',
            'Try to type this text quickly.'
        ]
    },
    'medium': {
        'ru': [
            'В современном мире скорость набора текста играет важную роль.',
            'Тренировка пальцев помогает улучшить навыки печати.',
            'Пора начинать тренировку!'
        ],
        'en': [
            'In the modern world, typing speed plays a crucial role.',
            'Finger exercises help improve typing skills.',
            'It is time to start training!'
        ]
    },
    'hard': {
        'ru': [
            'Современные технологии требуют высокой скорости печати.',
            'Чтобы стать профессионалом, необходимо много тренироваться.',
            'Давайте начнем сложную тренировку прямо сейчас!'
        ],
        'en': [
            'Modern technologies require high typing speed.',
            'To become a professional, you need to practice a lot.',
            'Let us start a challenging workout right now!'
        ]
    }
}

try:
    from PIL import ImageTk, Image
except ImportError:
    pass


class TypingTest(tk.Tk):
    """Класс, представляющий графическое приложение для теста скорости печати.

    Этот класс реализует графический интерфейс для тестирования скорости и точности печати,
    предоставляя пользователю текстовые задания на русском или английском языке с выбором уровня сложности.

    Атрибуты:
        start_time (float): Время начала теста.
        end_time (float): Время окончания теста.
        total_characters (int): Общее количество символов в задании.
        correct_characters (int): Количество правильных символов.
        wpm (int): Скорость печати (знаки в минуту).
        accuracy (int): Точность (в процентах).
        level (str): Уровень сложности теста ('easy', 'medium', 'hard').
        language (str): Язык текста ('ru', 'en').
    """

    def __init__(self):
        """Инициализация главного окна и элементов интерфейса.

        Здесь создаются все элементы пользовательского интерфейса, такие как метки, кнопки и поле ввода.
        Также инициализируются переменные для отслеживания времени, статистики и уровня сложности.
        """
        super().__init__()
        self.configure(bg='#E6F7FF')
        self.title('Тест скорости печати')
        self.geometry("800x600")

        # Переменные для отслеживания статистики
        self.start_time = None
        self.end_time = None
        self.total_characters = 0
        self.correct_characters = 0
        self.wpm = 0
        self.accuracy = 0

        # Текущий уровень сложности и язык
        self.level = 'easy'
        self.language = 'ru'
        self.ru_label = tk.Label(self, bg='#E6F7FF')
        self.ru_label.pack(padx=10, pady=20)

        # Меню для выбора уровня сложности и языка
        menu_frame = tk.Frame(self, bg='#E6F7FF')
        level_label = tk.Label(menu_frame, text='Уровень сложности:', bg='#E6F7FF')
        level_label.grid(row=0, column=0, padx=5, pady=5)
        self.level_var = tk.StringVar(value='easy')
        level_options = ['easy', 'medium', 'hard']
        level_menu = tk.OptionMenu(menu_frame, self.level_var,
                                   *level_options, command=self.change_level)
        level_menu.grid(row=0, column=1, padx=5, pady=5)

        language_label = tk.Label(menu_frame, text='Язык:', bg='#E6F7FF')
        language_label.grid(row=1, column=0, padx=5, pady=5)
        self.language_var = tk.StringVar(value='ru')
        language_options = ['ru', 'en']
        language_menu = tk.OptionMenu(menu_frame, self.language_var,
                                      *language_options, command=self.change_language)
        language_menu.grid(row=1, column=1, padx=5, pady=5)

        menu_frame.pack(side=tk.TOP, fill=tk.X)

        # Метка для отображения текста задания
        self.label_text = tk.Text(self, height=5, wrap=tk.WORD, font=('Arial', 18))
        self.label_text.tag_configure('green', foreground='green')
        self.label_text.tag_configure('red', foreground='red')
        self.label_text.pack(pady=30)

        # Поле ввода для ответа пользователя
        self.entry = tk.Entry(self, width=90)
        self.entry.bind('<KeyRelease>', self.on_key_release)
        self.entry.pack()

        # Кнопка для начала теста
        self.start_button = tk.Button(self, text='Начать тест', command=self.start_test)
        self.start_button.pack(pady=10)

        # Статистика
        self.stats_frame = tk.Frame(self)
        self.stats_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.stats_labels = []
        self.stats_frame.configure(bg='#E6F7FF')
        for i in range(6):
            label = tk.Label(self.stats_frame, text='', anchor=tk.W)
            label.grid(row=i, column=0, sticky=tk.W)
            self.stats_labels.append(label)

        self.update_text()

    def change_level(self, value):
        """Изменяет уровень сложности теста.

        Аргументы:
            value (str): Новый уровень сложности ('easy', 'medium', 'hard').
        """
        self.level = value
        self.update_text()

    def change_language(self, value):
        """Изменяет язык задания.

        Аргументы:
            value (str): Новый язык ('ru', 'en').
        """
        self.language = value
        self.update_text()

    def update_text(self):
        """Обновляет текст задания в зависимости от выбранного уровня сложности и языка.

        Метод выбирает случайный текст из списка для заданного уровня сложности и языка и отображает его
        в текстовом поле.
        """
        self.label_text.delete('1.0', tk.END)
        self.label_text.insert(tk.END, choice(texts[self.level][self.language]))

    def on_key_release(self, event):
        """Обрабатывает ввод с клавиатуры и проверяет символы.

        Каждый раз, когда пользователь нажимает клавишу, метод сравнивает введенные символы с правильными
        и окрашивает их в зеленый или красный цвет в зависимости от того, правильный ли был символ.

        Аргументы:
            event (tk.Event): Событие, которое происходит при отпускании клавиши.
        """
        if not self.start_time:
            return

        current_text = self.entry.get()
        target_text = self.label_text.get('1.0', tk.END).strip()

        # Сбрасываем счётчики для пересчёта
        self.correct_characters = 0

        # Сравниваем символы
        for index, char in enumerate(current_text):
            try:
                if char == target_text[index]:
                    self.label_text.tag_add('green', f'1.{index}', f'1.{index+1}')
                    self.correct_characters += 1
                else:
                    self.label_text.tag_add('red', f'1.{index}', f'1.{index+1}')
            except IndexError:
                break

        self.calculate_stats()

    def calculate_stats(self):
        """Вычисляет статистику: время, скорость печати и точность.

        Метод рассчитывает время, количество правильных символов, скорость печати (WPM) и точность
        (процент правильных символов) и отображает эти данные в интерфейсе.
        """
        elapsed_time = perf_counter() - self.start_time
        total_characters = len(self.label_text.get('1.0', tk.END).strip())
        entered_characters = len(self.entry.get())
        correct_characters = self.correct_characters
        wpm = int(correct_characters / (elapsed_time / 60)) if elapsed_time > 0 else 0
        accuracy = int((correct_characters / total_characters) * 100) if total_characters > 0 else 0

        self.stats_labels[0].config(text=f'Время: {int(elapsed_time)} сек.', bg='#E6F7FF')
        self.stats_labels[1].config(text=f'Скорость (знаки/мин): {wpm}', bg='#E6F7FF')
        self.stats_labels[2].config(text=f'Точность: {accuracy}%', bg='#E6F7FF')
        self.stats_labels[3].config(text=f'Общее количество введенных знаков: {entered_characters}', bg='#E6F7FF')
        self.stats_labels[4].config(text=f'Количество правильных введенных знаков: {correct_characters}', bg='#E6F7FF')
        self.stats_labels[5].config(text=f'Общее количество знаков в тексте: {total_characters}', bg='#E6F7FF')

    def start_test(self):
        """Запускает новый тест.

        Этот метод запускает новый тест, сбрасывает время и статистику, а также очищает поле ввода.
        """
        self.start_time = perf_counter()
        self.entry.focus_set()
        self.entry.delete(0, tk.END)
        self.correct_characters = 0
        self.total_characters = len(self.label_text.get('1.0', tk.END).strip())
        self.calculate_stats()


if __name__ == '__main__':
    app = TypingTest()
    app.mainloop()
