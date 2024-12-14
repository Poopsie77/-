from unittest.mock import patch, MagicMock
import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import pygame
import random
from time import perf_counter
import string
import unittest

# Путь до папки "apps"
apps_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'apps'))
# Добавляем путь к папке "apps" в sys.path
sys.path.insert(0, apps_path)


from app import AppLauncher
from apps.Падающие_буквы import FallingLetter, generate_falling_letter, select_time, HEIGHT
from apps.Тренажер_печати import TypingTest  # Замените на правильный путь к вашему модулю


class TestAppLauncher(unittest.TestCase): #app.py

    @patch('os.listdir')
    def test_get_apps_list_success(self, mock_listdir):
        """Тестирует корректное получение списка приложений"""
        mock_listdir.return_value = ['app1.py', 'app2.py', 'not_app.txt']
        app = AppLauncher()
        app.apps_dir = 'test_dir'
        result = app.get_apps_list()
        self.assertEqual(result, ['app1.py', 'app2.py'])

    @patch('os.listdir')
    @patch('tkinter.messagebox.showerror')
    def test_get_apps_list_folder_not_found(self, mock_showerror, mock_listdir):
        """Тестирует ошибку, если папка с приложениями не найдена"""
        mock_listdir.side_effect = FileNotFoundError
        app = AppLauncher()
        app.apps_dir = 'non_existent_folder'
        result = app.get_apps_list()
        self.assertEqual(result, [])
        mock_showerror.assert_called_with('Ошибка', 'Папка non_existent_folder не найдена.')

    @patch('subprocess.Popen')
    def test_run_app_success(self, mock_popen):
        """Тестирует успешный запуск приложения"""
        app = AppLauncher()
        app.apps_dir = 'test_dir'
        mock_popen.return_value = MagicMock()
        app.run_app('app1.py')
        mock_popen.assert_called_with(['python', os.path.join('test_dir', 'app1.py')])

    @patch('subprocess.Popen')
    @patch('tkinter.messagebox.showerror')
    def test_run_app_failure(self, mock_showerror, mock_popen):
        """Тестирует ошибку при запуске приложения"""
        mock_popen.side_effect = Exception("Ошибка запуска")
        app = AppLauncher()
        app.apps_dir = 'test_dir'
        app.run_app('app1.py')
        mock_showerror.assert_called_with('Ошибка', 'Не удалось запустить приложение: Ошибка запуска')

class TestGame(unittest.TestCase): #Падающие_буквы.py
    # Мокаем pygame
    @patch('pygame.display.set_mode')
    @patch('pygame.display.flip')
    @patch('pygame.image.load')
    @patch('pygame.font.Font')
    @patch('pygame.event.get', return_value=[])
    def test_generate_falling_letter(self, mock_event, mock_font, mock_image_load, mock_flip, mock_set_mode):
        """Проверяем, что функция generate_falling_letter генерирует корректные буквы."""

        # Мокаем возвращаемое значение для генерации случайной буквы
        mock_set_mode.return_value = MagicMock()  # Мокаем экран
        mock_image_load.return_value = MagicMock()  # Мокаем изображение
        mock_font.return_value = MagicMock()  # Мокаем шрифт

        # Генерируем букву для уровня сложности 1 (строчные буквы)
        letter_obj = generate_falling_letter(difficulty=1)
        self.assertIn(letter_obj.letter, string.ascii_lowercase)  # Проверяем, что это строчная буква

        # Генерируем букву для уровня сложности 2 (заглавные буквы)
        letter_obj = generate_falling_letter(difficulty=2)
        self.assertIn(letter_obj.letter, string.ascii_uppercase)  # Проверяем, что это заглавная буква

        # Генерируем букву для уровня сложности 3 (все печатаемые символы)
        letter_obj = generate_falling_letter(difficulty=3)
        self.assertIn(letter_obj.letter, string.printable[:-6])  # Проверяем, что это печатный символ

    @patch('pygame.display.flip')  # Мокаем flip
    @patch('pygame.font.Font')  # Мокаем шрифт
    def test_falling_letter(self, mock_font, mock_flip):
        """Проверяем поведение объекта FallingLetter."""

        # Создаем объект FallingLetter
        letter = FallingLetter(x=100, y=100, letter="A")

        # Проверяем начальные значения
        self.assertEqual(letter.x, 100)
        self.assertEqual(letter.y, 100)
        self.assertEqual(letter.letter, "A")
        self.assertIsInstance(letter.speed, int)  # Проверяем, что скорость — это целое число

        # Мокаем функции
        mock_font.return_value = MagicMock()  # Мокаем шрифт

        # Проверяем движение буквы
        letter.move()
        self.assertGreater(letter.y, 100)  # Проверяем, что буква двигается вниз

        # Проверяем, что буква покинула экран
        letter.y = HEIGHT + 1  # Устанавливаем букву за пределы экрана
        self.assertTrue(letter.is_off_screen())  # Проверяем, что is_off_screen возвращает True


    @patch('pygame.event.get')
    def test_main_game_logic(self, mock_event):
        """Тестируем логику игры без запуска самой игры."""

        # Мокаем события
        mock_event.return_value = [
            pygame.event.Event(pygame.KEYDOWN, {'unicode': 'a'}),
            pygame.event.Event(pygame.QUIT)
        ]

        falling_letters = [FallingLetter(x=100, y=100, letter='a')]
        score = 0
        missed = 0
        time_left = 10  # Устанавливаем время на 10 секунд

        # Процесс обработки одного шага игры (в реальной игре бы выполнялся цикл)
        for event in mock_event.return_value:
            if event.type == pygame.KEYDOWN:
                typed_char = event.unicode.lower()
                found_match = False
                for letter in falling_letters:
                    if letter.letter == typed_char:
                        falling_letters.remove(letter)
                        score += 1
                        found_match = True
                        break
                if not found_match:
                    time_left -= 5  # Уменьшаем время на 5 секунд при неправильном вводе

        # Проверяем, что буква удаляется и счёт увеличивается
        self.assertEqual(score, 1)
        self.assertEqual(time_left, 10)  # Никаких других изменений времени


class TestTypingTest(unittest.TestCase):

    def setUp(self):
        """Настройка объекта приложения."""
        self.test_app = TypingTest()  # Теперь класс должен быть найден


    def test_on_key_release(self):
        """Тестирование on_key_release."""
        # Ваш тест здесь
        self.test_app.on_key_release('a')  # Пример вызова метода

    def test_start_test(self):
        """Тестирование старта теста."""
        self.test_app.start_test()
        self.assertTrue(self.test_app.start_time)  # Пример проверки



if __name__ == '__main__':
    unittest.main()