import tkinter as tk
from tkinter import messagebox
import os
import subprocess
from PIL import ImageTk, Image

class AppLauncher(tk.Tk):
    """
    Класс приложения-загрузчика, который предоставляет графический интерфейс
    для запуска других приложений, находящихся в указанной папке.
    """

    def __init__(self, apps_dir='apps', images_dir='images'):
        super().__init__()
        self.apps_dir = apps_dir
        self.images_dir = images_dir  # Папка для изображений
        self.title('Приложение-загрузчик')
        self.geometry('900x600')
        self.configure(bg='#abe9dc')  # Цвет фона в новогоднем стиле
        self.resizable(False, False)

        self.load_background_image()
        self.create_widgets()

    def load_background_image(self):
        """
        Загружает фоновое изображение, если оно доступно.
        """
        try:
            # Путь к изображению в папке images относительно местоположения текущего скрипта
            background_image_path = os.path.join(os.path.dirname(__file__), self.images_dir, 'happy.jpg')
            print(f"Путь к изображению: {background_image_path}")  # Отладочное сообщение
            background_image = Image.open(background_image_path)
            resized_bg = background_image.resize((900, 600), Image.Resampling.LANCZOS)
            self.background = ImageTk.PhotoImage(resized_bg)
            self.bg_label = tk.Label(self, image=self.background)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except (IOError, AttributeError) as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить фоновое изображение: {e}")

    def create_widgets(self):
        """
        Создает виджеты для приветственного окна.
        """
        self.welcome_label = tk.Label(self, text='Добро пожаловать!', font=("Arial", 24), fg="#006400", bg='#abe9dc')
        self.welcome_label.place(x=325, y=230)

        self.start_button = tk.Button(self, text='Начать', command=self.show_apps_menu)
        self.start_button.place(x=440, y=300)

    def show_apps_menu(self):
        """
        Отображает меню с доступными приложениями для запуска.
        """
        self.welcome_label.destroy()
        self.start_button.destroy()

        apps_list = self.get_apps_list()
        frame = tk.Frame(self, bg='#abe9dc')
        frame.pack(expand=True)

        for i, app_name in enumerate(apps_list):
            app_display_name = os.path.splitext(app_name)[0]
            button = tk.Button(
                frame,
                text=f'Запустить {app_display_name}',
                command=lambda app=app_name: self.run_app(app),
                bg='#abe9dc'
            )
            button.grid(row=i, column=0, pady=15)

    def get_apps_list(self):
        """
        Получает список доступных приложений для запуска.
        """
        try:
            # Путь к папке приложений относительно местоположения текущего скрипта
            apps_list = [f for f in os.listdir(os.path.join(os.path.dirname(__file__), self.apps_dir)) if f.endswith('.py')]
        except FileNotFoundError:
            apps_list = []
            messagebox.showerror('Ошибка', f'Папка {self.apps_dir} не найдена.')
        return apps_list

    def run_app(self, app_name):
        """
        Запускает указанное приложение.
        """
        app_path = os.path.join(os.path.dirname(__file__), self.apps_dir, app_name)
        try:
            subprocess.Popen(['python', app_path])
        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось запустить приложение: {e}')

if __name__ == '__main__':
    app = AppLauncher()
    app.mainloop()
