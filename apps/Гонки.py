import pygame
import sys
import random
from time import perf_counter
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def init_game(road_image_path='../images/road.png',  # Путь с учетом папки images
              car1_image_path='../images/car1.png',
              car2_image_path='../images/car2.png',
              win_background_path='../images/road.png'):
    """
    Инициализация игры, загрузка изображений и настройка экрана.
    """
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Gonki")

    try:
        # Загрузка изображений
        road_image = pygame.transform.scale(pygame.image.load(road_image_path), (1200, 800)).convert_alpha()
        win_background = pygame.transform.scale(pygame.image.load(win_background_path), (1200, 800)).convert_alpha()
    except FileNotFoundError:
        print("Не удалось найти файл изображения.")
        sys.exit(1)

    return screen, road_image, win_background

def generate_text():
    """
    Генерирует случайный текст для ввода пользователем или ботом.
    """
    return random.choice([  # Генерация случайного текста
        "Вперед и только вперед!", "Сегодня отличный день!", "Ускорься, чтобы выиграть!",
        "Осталось немного до финиша!", "Поехали, держись!", "Впереди победа!",
        "Не останавливайся!", "Время показать мастерство!", "Твой успех зависит от тебя!",
        "Ты справишься, верь в себя!"
    ])

def display_winner(screen, win_background, winner_text):
    """
    Отображает экран победы.
    """
    font_big = pygame.font.Font(None, 64)
    winner_surface = font_big.render(winner_text, True, (255, 255, 255))
    restart_surface = font_big.render("Нажмите R для перезапуска или Q для выхода", True, (255, 255, 255))

    winner_rect = winner_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    restart_rect = restart_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

    screen.fill((0, 0, 0))
    screen.blit(win_background, (0, 0))
    screen.blit(winner_surface, winner_rect)
    screen.blit(restart_surface, restart_rect)
    pygame.display.flip()

def game_loop():
    """
    Основной игровой цикл.
    """
    # Инициализация игры с относительными путями
    screen, road_image, win_background = init_game()
    cars = [
        {
            'image': pygame.transform.scale(pygame.image.load('../images/car1.png'), (80, 160)),  # Путь с учетом папки images
            'x': 50, 'y': 450, 'speed': 0.6, 'input_text': '', 'target_text': '', 'last_key_time': perf_counter(), 'cooldown': 1, 'velocity': 0, 'is_bot': False
        },
        {
            'image': pygame.transform.scale(pygame.image.load('../images/car2.png'), (80, 160)),
            'x': 50, 'y': 650, 'speed': 0.2, 'input_text': '', 'target_text': '', 'last_key_time': perf_counter(), 'cooldown': 2, 'velocity': 0, 'is_bot': True
        }
    ]

    font = pygame.font.Font(None, 32)
    input_box_player = pygame.Rect(350, 10, 600, 30)
    input_text_player = pygame.Rect(440, 50, 400, 30)

    end_position = 1200 - 80  # Конец дороги

    # Генерация начального текста для ввода
    for car in cars:
        car['target_text'] = generate_text()

    game_over = False
    active_car = 0
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)

        # Отображение дороги
        screen.blit(road_image, (0, 0))

        # Отображение текстовых полей
        pygame.draw.rect(screen, (255, 255, 255), input_box_player, 0)
        pygame.draw.rect(screen, (255, 255, 255), input_text_player, 0)
        target_text_surface = font.render(cars[0]['target_text'], True, (0, 0, 0))
        input_text_surface = font.render(cars[0]['input_text'], True, (0, 0, 0))
        screen.blit(target_text_surface, (input_box_player.x + 5, input_box_player.y + 5))
        screen.blit(input_text_surface, (input_text_player.x + 5, input_text_player.y + 5))

        # Отображение машин
        for car in cars:
            screen.blit(car['image'], (car['x'], car['y']))

        # Логика для бота
        for car in cars:
            if car['is_bot']:
                if len(car['input_text']) < len(car['target_text']):
                    car['input_text'] += car['target_text'][len(car['input_text'])]
                    car['last_key_time'] = perf_counter()
                else:
                    car['input_text'] = ''
                    car['target_text'] = generate_text()

        # Обработка событий (ввод с клавиатуры)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    active_car = (active_car + 1) % len(cars)
                elif event.key == pygame.K_RETURN:
                    cars[active_car]['input_text'] = ''
                    cars[active_car]['target_text'] = generate_text()
                elif event.key == pygame.K_BACKSPACE:
                    cars[active_car]['input_text'] = cars[active_car]['input_text'][:-1]
                elif event.key == pygame.K_r and game_over:
                    return
                elif event.key == pygame.K_q and game_over:
                    pygame.quit()
                    sys.exit()
                else:
                    cars[active_car]['input_text'] += event.unicode
                    cars[active_car]['last_key_time'] = perf_counter()

        # Рассчитываем скорость машины на основе правильных и неправильных символов
        for car in cars:
            correct_chars = sum([1 for i in range(min(len(car['input_text']), len(car['target_text']))) if car['input_text'][i] == car['target_text'][i]])
            mistakes = len(car['target_text']) - correct_chars
            car['velocity'] = max(0, 2 - 0.1 * mistakes)

        # Двигаем машины по экрану
        for car in cars:
            car['x'] += car['velocity']

        # Проверка на победителя
        for car in cars:
            if car['x'] + 80 >= end_position:
                winner_text = "Выиграл пользователь!" if not car['is_bot'] else "Выиграл бот!"
                game_over = True
                display_winner(screen, win_background, winner_text)

                pygame.display.flip()

                # Ожидание ввода для перезапуска или выхода
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                waiting = False
                                game_loop()
                            elif event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit(0)

        pygame.display.flip()

# Запуск игры
game_loop()
