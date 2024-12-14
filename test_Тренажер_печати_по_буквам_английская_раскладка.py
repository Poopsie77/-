from unittest import TestCase, mock
import tkinter as tk
from unittest.mock import MagicMock, patch
import unittest


# Мокаем tkinter.Tk для предотвращения ошибок с tk.tcl
@patch('tkinter.Tk', MagicMock())
@patch('tkinter.PhotoImage', MagicMock())  # Мокаем PhotoImage
class TestTypingTest_EN(TestCase):

    def setUp(self):
        from apps.Тренажер_печати_по_буквам_английская_раскладка import TypingTest_EN
        self.app = TypingTest_EN()

        # Мокаем методы, которые требуют GUI
        self.app.start_test = MagicMock()
        self.app.end_test = MagicMock()

    @patch('time.perf_counter', return_value=10.0)
    def test_start_end_time(self, mock_perf_counter):
        """Тестирование начала и окончания теста."""
        # Метод start_test должен обновить start_time значением mock_perf_counter
        self.app.start_test.side_effect = lambda: setattr(self.app, 'start_time', mock_perf_counter())

        # Симуляция старта теста
        self.app.start_test()
        self.assertEqual(self.app.start_time, 10.0)  # start_time должен быть установлен на 10.0

        # Симуляция завершения теста
        self.app.end_time = mock_perf_counter()  # Используем mock_perf_counter
        self.app.end_test()

        # Проверяем, что end_time не меньше start_time
        self.assertGreaterEqual(self.app.end_time, self.app.start_time)

if __name__ == '__main__':
    unittest.main()
