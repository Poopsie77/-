import pygame
import sys
import random
import string
import os  # Для работы с путями

# Настройки окна
WIDTH = 1080
HEIGHT = 720
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тренажер для набора текста")
clock = pygame.time.Clock()

# Шрифт
font = pygame.font.SysFont(None, 48)

# Кэш шрифтов
cached_fonts = {}

def get_cached_font(size):
    """
    Возвращает кэшированный шрифт для указанного размера.

    Если шрифт для данного размера уже был создан, он берется из кэша. Если нет, создается новый и добавляется в кэш.

    Args:
        size (int): Размер шрифта.

    Returns:
        pygame.font.Font: Объект шрифта.
    """
    global cached_fonts
    if size not in cached_fonts:
        cached_fonts[size] = pygame.font.Font(None, size)
    return cached_fonts[size]


# Загрузка фонового изображения
base_dir = os.path.dirname(os.path.abspath(__file__))  # Путь до текущей директории (где находится ваш скрипт)
background_image_path = os.path.join(base_dir, '..', 'images', 'background.jpg')  # Путь к изображению

# Печатаем путь для проверки
print("Путь к изображению:", background_image_path)

background_image = pygame.image.load(background_image_path).convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


class FallingLetter:
    """
    Класс для создания падающих букв на экране.
    """

    def __init__(self, x, y, letter):
        """
        Инициализация объекта FallingLetter.

        Args:
            x (int): Начальная координата по оси X.
            y (int): Начальная координата по оси Y.
            letter (str): Буква, которая будет падать.
        """
        self.x = x
        self.y = y
        self.letter = letter
        self.speed = random.randint(1, 3)

    def draw(self):
        """
        Отображает букву на экране.
        """
        text_surface = get_cached_font(79).render(self.letter, True, BLACK)
        screen.blit(text_surface, (self.x, self.y))

    def move(self):
        """
        Двигает букву вниз по экрану.
        """
        self.y += self.speed

    def is_off_screen(self):
        """
        Проверяет, покинула ли буква экран.

        Returns:
            bool: True, если буква покинула экран, иначе False.
        """
        return self.y > HEIGHT


def generate_falling_letter(difficulty=1):
    """
    Генерирует новую падающую букву в зависимости от уровня сложности.

    Args:
        difficulty (int): Уровень сложности:
            - 1: строчные буквы,
            - 2: заглавные буквы,
            - 3: все печатаемые символы (без управляющих символов).

    Returns:
        FallingLetter: Объект класса FallingLetter с случайной буквой.
    """
    x = random.randint(0, WIDTH - 50)
    y = -50

    if difficulty == 1:
        letters = string.ascii_lowercase
    elif difficulty == 2:
        letters = string.ascii_uppercase
    else:
        letters = string.printable[:-6]  # Все печатаемые символы без управляющих символов

    letter = random.choice(letters)
    return FallingLetter(x, y, letter)


def select_time():
    """
    Экран выбора времени игры.

    Отображает интерфейс с тремя кнопками для выбора времени игры: 1 минута, 3 минуты, 5 минут.

    Returns:
        int: Выбранное время игры в секундах (60, 180 или 300 секунд).
    """
    screen.blit(background_image, (0, 0))  # Отображаем фон
    title_text = get_cached_font(72).render("Выберите продолжительность игры:", True, BLACK)
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, 150))  # Центрируем заголовок

    button_width, button_height = 200, 60  # Размеры кнопок
    button_x = (WIDTH - button_width) // 2  # Горизонтальный центр

    # Определяем кнопки с учетом вертикального отступа
    one_minute_button = pygame.Rect(button_x, 300, button_width, button_height)
    three_minutes_button = pygame.Rect(button_x, 400, button_width, button_height)
    five_minutes_button = pygame.Rect(button_x, 500, button_width, button_height)

    # Рисуем кнопки
    pygame.draw.rect(screen, GREEN, one_minute_button)
    pygame.draw.rect(screen, YELLOW, three_minutes_button)
    pygame.draw.rect(screen, RED, five_minutes_button)

    # Подписи на кнопках
    one_minute_label = get_cached_font(36).render("1 минута", True, WHITE)
    three_minutes_label = get_cached_font(36).render("3 минуты", True, WHITE)
    five_minutes_label = get_cached_font(36).render("5 минут", True, WHITE)

    # Центрируем текст на кнопках
    screen.blit(one_minute_label, (one_minute_button.centerx - one_minute_label.get_width() // 2,
                                   one_minute_button.centery - one_minute_label.get_height() // 2))
    screen.blit(three_minutes_label, (three_minutes_button.centerx - three_minutes_label.get_width() // 2,
                                      three_minutes_button.centery - three_minutes_label.get_height() // 2))
    screen.blit(five_minutes_label, (five_minutes_button.centerx - five_minutes_label.get_width() // 2,
                                     five_minutes_button.centery - five_minutes_label.get_height() // 2))

    pygame.display.flip()

    selected_time = None
    while selected_time is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if one_minute_button.collidepoint(mouse_pos):
                    selected_time = 60
                elif three_minutes_button.collidepoint(mouse_pos):
                    selected_time = 180
                elif five_minutes_button.collidepoint(mouse_pos):
                    selected_time = 300

    return selected_time


def main():
    """
    Основная функция игры.

    Запускает игровой цикл, отображает падающие буквы, обрабатывает ввод пользователя,
    обновляет счет, и завершает игру по истечении времени.
    """
    running = True
    while running:
        falling_letters = []
        score = 0
        missed = 0
        time_left = select_time()  # Выбор времени игры

        while True:
            clock.tick(FPS)

            # События
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
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

            # Генерация новых букв
            if len(falling_letters) < 7:
                falling_letters.append(generate_falling_letter())

            # Движение букв
            for letter in falling_letters:
                letter.move()
                if letter.is_off_screen():
                    falling_letters.remove(letter)
                    missed += 1

            # Уменьшение оставшегося времени
            time_left -= 1 / FPS
            if time_left <= 0:
                break

            # Отображение информации
            screen.blit(background_image, (0, 0))  # Отображаем фон
            for letter in falling_letters:
                letter.draw()

            score_text = get_cached_font(48).render(f"Счёт: {score}", True, GREEN)
            screen.blit(score_text, (10, 10))

            missed_text = get_cached_font(48).render(f"Пропущено: {missed}", True, RED)
            screen.blit(missed_text, (10, 70))

            time_text = get_cached_font(48).render(f"Оставшееся время: {int(time_left):02d}", True, BLACK)
            screen.blit(time_text, (10, 130))

            pygame.display.flip()

        # Окончание игры
        game_over_text = get_cached_font(48).render("Игра окончена! Нажмите любую клавишу для перезапуска.", True,
                                                    BLACK)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    break
            pygame.display.flip()


if __name__ == "__main__":
    main()
