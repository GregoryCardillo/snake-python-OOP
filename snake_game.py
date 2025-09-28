import curses
import random

# Snake class
class Snake:
    def __init__(self):
        self.body = [(10, 10), (10, 9), (10, 8)]  # Initial snake position (y, x)
        self.direction = curses.KEY_RIGHT  # Snake starts moving right
        self.grow = False  # Flag to indicate if the snake should grow

    def move(self):
        head_y, head_x = self.body[0]
        if self.direction == curses.KEY_UP:
            new_head = (head_y - 1, head_x)
        elif self.direction == curses.KEY_DOWN:
            new_head = (head_y + 1, head_x)
        elif self.direction == curses.KEY_LEFT:
            new_head = (head_y, head_x - 1)
        elif self.direction == curses.KEY_RIGHT:
            new_head = (head_y, head_x + 1)

        self.body = [new_head] + self.body[:-1] if not self.grow else [new_head] + self.body
        self.grow = False

    def grow_snake(self):
        self.grow = True  # Mark the snake for growth

    def get_head(self):
        return self.body[0]

    def get_body(self):
        return self.body

# Food class
class Food:
    def __init__(self, max_y, max_x):
        self.position = (random.randint(1, max_y - 2), random.randint(1, max_x - 2))  # Avoid borders
    
    def spawn(self, max_y, max_x):
        self.position = (random.randint(1, max_y - 2), random.randint(1, max_x - 2))  # Avoid borders
    
    def get_position(self):
        return self.position

# Game class
class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.snake = Snake()
        self.food = Food(*stdscr.getmaxyx())
        self.score = 0
        self.max_y, self.max_x = stdscr.getmaxyx()

    def draw(self):
        self.stdscr.clear()  # Clear the screen
        self.stdscr.border(0)  # Draw the border
        self.stdscr.addstr(0, 2, f"Score: {self.score}")  # Show the score

        # Draw the snake
        for y, x in self.snake.get_body():
            self.stdscr.addstr(y, x, "■", curses.color_pair(1))  # Drawing snake (no multiplication for x)

        # Draw the food
        food_y, food_x = self.food.get_position()
        self.stdscr.addstr(food_y, food_x, "◆", curses.color_pair(2))  # Drawing food (no multiplication for x)

        self.stdscr.refresh()  # Refresh the screen

    def handle_input(self):
        key = self.stdscr.getch()
        if key == 27:  # ESC key to quit
            return False
        elif key == curses.KEY_UP and self.snake.direction != curses.KEY_DOWN:
            self.snake.direction = curses.KEY_UP
        elif key == curses.KEY_DOWN and self.snake.direction != curses.KEY_UP:
            self.snake.direction = curses.KEY_DOWN
        elif key == curses.KEY_LEFT and self.snake.direction != curses.KEY_RIGHT:
            self.snake.direction = curses.KEY_LEFT
        elif key == curses.KEY_RIGHT and self.snake.direction != curses.KEY_LEFT:
            self.snake.direction = curses.KEY_RIGHT
        return True

    def check_collisions(self):
        head_y, head_x = self.snake.get_head()
        # Check if the snake collides with the walls
        if head_y == 0 or head_x == 0 or head_y == self.max_y - 1 or head_x == self.max_x - 1:
            return True
        # Check if the snake collides with itself
        if (head_y, head_x) in self.snake.get_body()[1:]:
            return True
        return False

    def check_food(self):
        head_y, head_x = self.snake.get_head()
        food_y, food_x = self.food.get_position()
        if (head_y, head_x) == (food_y, food_x):
            self.snake.grow_snake()
            self.score += 1
            self.food.spawn(self.max_y, self.max_x)  # Respawn food

    def game_loop(self):
        while True:
            self.draw()
            self.snake.move()
            self.check_food()

            if self.check_collisions():
                break  # Game Over

            if not self.handle_input():
                break  # Exit on ESC key

            curses.napms(50)  # Reduced delay to improve responsiveness

def main(stdscr):
    # Initialize the window
    curses.curs_set(0)  # Hide cursor
    curses.start_color()  # Start color support
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Food color
    stdscr.timeout(100)  # Set timeout to allow non-blocking input (100ms delay)
    game = SnakeGame(stdscr)
    game.game_loop()

if __name__ == "__main__":
    curses.wrapper(main)
