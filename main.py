import pygame
import random

# Размеры игрового поля
FIELD_WIDTH = 20
FIELD_HEIGHT = 20
CELL_SIZE = 20

# Размеры окна
WINDOW_WIDTH = FIELD_WIDTH * CELL_SIZE
WINDOW_HEIGHT = FIELD_HEIGHT * CELL_SIZE

# Направления движения змейки
# Каждому направлению соответствует смещение по x и y
DIRECTIONS = {
    pygame.K_w: (0, -1),  # Вверх
    pygame.K_s: (0, 1),   # Вниз
    pygame.K_a: (-1, 0),  # Влево
    pygame.K_d: (1, 0)    # Вправо
}

# Количество еды, необходимое для победы
REQUIRED_FOOD = 10

class Snake:
    def __init__(self):
        # Тело змейки - список координат ее сегментов
        self.body = [(10, 10)]
        # Направление движения змейки
        self.direction = (0, 1)  # Изначально змейка движется вниз
        # Флаг, указывающий, должна ли змейка увеличиться при следующем ходе
        self.grow = False

    def move(self):
        """
        Метод для перемещения змейки на один шаг.
        Возвращает False, если змейка врезалась в себя.
        """
        # Получаем координаты головы змейки
        head_x, head_y = self.body[0]
        # Получаем смещение в соответствии с текущим направлением движения
        dx, dy = self.direction
        # Вычисляем новые координаты головы змейки с учетом обхода границ поля
        new_head = (
            (head_x + dx) % FIELD_WIDTH,
            (head_y + dy) % FIELD_HEIGHT
        )

        # Проверяем, не врезалась ли змейка в свое тело
        if new_head in self.body[1:]:
            return False

        # Добавляем новую голову змейки
        self.body.insert(0, new_head)
        # Если змейка не должна увеличиваться, удаляем ее хвост
        if not self.grow:
            self.body.pop()
        else:
            # Сбрасываем флаг роста
            self.grow = False

        return True

    def turn(self, direction):
        """
        Метод для поворота змейки.
        Проверяет, чтобы змейка не поворачивала в обратном направлении.
        """
        # Проверяем, чтобы змейка не поворачивала в обратном направлении
        if direction == pygame.K_w and self.direction == (0, 1):
            return
        elif direction == pygame.K_s and self.direction == (0, -1):
            return
        elif direction == pygame.K_a and self.direction == (1, 0):
            return
        elif direction == pygame.K_d and self.direction == (-1, 0):
            return

        # Меняем направление движения змейки
        self.direction = DIRECTIONS[direction]

    def eat(self):
        """
        Метод, вызываемый, когда змейка съедает еду.
        Устанавливает флаг роста, чтобы змейка увеличилась при следующем ходе.
        """
        self.grow = True

class Game:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()
        # Создание окна игры
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # Установка заголовка окна
        pygame.display.set_caption("Snake Game")
        # Создание часов для контроля FPS
        self.clock = pygame.time.Clock()

        # Создание змейки
        self.snake = Snake()
        # Генерация начальной еды
        self.food = self.generate_food()
        # Счет игрока
        self.score = 0

    def generate_food(self):
        """
        Метод для генерации новой еды на поле.
        Координаты еды не должны совпадать с координатами змейки.
        """
        while True:
            food_x = random.randint(0, FIELD_WIDTH - 1)
            food_y = random.randint(0, FIELD_HEIGHT - 1)
            if (food_x, food_y) not in self.snake.body:
                return (food_x, food_y)

    def draw_field(self):
        """

        Метод для отрисовки игрового поля.
        Отрисовывает змейку, еду и счет игрока.
        """
        self.screen.fill((0, 0, 0))  # Очистка экрана

        # Отрисовка сегментов змейки
        for x, y in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
# Отрисовка еды
        pygame.draw.rect(self.screen, (255, 0, 0), (self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Отрисовка счета игрока
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        pygame.display.flip()  # Обновление экрана

    def play(self):
        """
        Главный игровой цикл.
        Обрабатывает события, перемещает змейку, проверяет столкновения и условия победы.
        """
        while True:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key in DIRECTIONS:
                        self.snake.turn(event.key)

            # Перемещение змейки
            if not self.snake.move():
                print("Game Over!")
                break

            # Проверка, если змейка съела еду
            if self.snake.body[0] == self.food:
                self.snake.eat()
                self.food = self.generate_food()
                self.score += 1

                # Проверка условия победы
                if self.score >= REQUIRED_FOOD:
                    print("You win!")
                    break

            # Отрисовка игрового поля
            self.draw_field()
            self.clock.tick(10)  # Ограничение FPS

if __name__ == "__main__":
    game = Game()
    game.play()
