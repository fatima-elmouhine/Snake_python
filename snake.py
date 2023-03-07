import pygame
import sys
import random

class Block:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

class Food:
    def __init__(self):
        x = random.randint(0, nbr_col - 1)
        y = random.randint(0, nbr_row - 1)
        self.block = Block(x, y)
        
    def draw_food(self):
        rect = pygame.Rect(self.block.x * cell_size, self.block.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, pygame.Color('green'), rect)

class Snake:
    def __init__(self):
        self.body = [Block(5, 5)]
        self.direction = 'RIGHT'   
    def draw_snake(self):
        for block in self.body:
            x_coord = block.x * cell_size
            y_coord = block.y * cell_size
            block_rect = pygame.Rect(x_coord, y_coord, cell_size, cell_size)
            pygame.draw.rect(screen, pygame.Color('red'), block_rect)
            
    def move_snake(self):
        snake_body_count = len(self.body)
        old_head = self.body[snake_body_count-1]
        
        if self.direction == 'RIGHT':
            new_head = Block(old_head.x + 1, old_head.y)
        elif self.direction == 'LEFT':
            new_head = Block(old_head.x - 1, old_head.y)
        elif self.direction == 'TOP':
            new_head = Block(old_head.x, old_head.y - 1)
        else:
            new_head = Block(old_head.x, old_head.y + 1)
            
        # ajoute nouveau elmt a la fin de la liste du body
        self.body.append(new_head)
        # # retire le premier element de la liste
        # self.body.pop(0)

    def resetSnake(self):
        self.body = [Block(5, 5)]
        self.direction = 'RIGHT'

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.generate_food()
        self.score = 0
        
    def update(self):
        self.snake.move_snake()
        self.check_collision()  
        self.game_over()       
        
    def draw_elements(self):
        self.food.draw_food()
        self.snake.draw_snake()
        
    def check_collision(self):
        snake_length = len(self.snake.body)
        snake_head_position = self.snake.body[snake_length - 1]
        food_position = self.food.block
        
        if snake_head_position.x == food_position.x and snake_head_position.y == food_position.y:
            self.generate_food()
        else:
            self.snake.body.pop(0)
        
    def generate_food(self):
        
        should_generate_food = True
        while should_generate_food:
            count = 0
            for block in self.snake.body:
                if block.x == self.food.block.x and block.y == self.food.block.y:
                    count += 1
                
            if count == 0:
                should_generate_food = False
            else:
                self.food = Food()
       
    def game_over(self):
        snake_length = len(self.snake.body)
        snake_head_position = self.snake.body[snake_length - 1]
        
        if (snake_head_position.x not in range(0,nbr_col) or (snake_head_position.y not in range(0,nbr_row))):
            print('game over')
            self.snake.resetSnake()

        
        # au cas ou le serpent mord sa queue
        for block in self.snake.body[0:snake_length -1]:
            if snake_head_position.x == block.x and snake_head_position.y == block.y:
                print('game over')
                self.snake.resetSnake()

            
           
pygame.init()

nbr_col = 10
nbr_row = 15
cell_size = 50

screen = pygame.display.set_mode(size=(nbr_col * cell_size, nbr_row * cell_size))
timer = pygame.time.Clock()

game_on = True

def draw_grid():
    for i in range(0,nbr_col):
        for j in range(0, nbr_row):
            rect = pygame.Rect(i * cell_size, j * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, pygame.Color('black'), rect, 1)
            

game = Game()

# custom event
screen_update = pygame.USEREVENT
# tout les 200 millisecondes on declenche l'evenement screen_update
pygame.time.set_timer(screen_update, 150)

while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
            sys.exit()
        
        if event.type == screen_update:
            game.update()
        
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_LEFT:
                if game.snake.direction != 'RIGHT':
                    game.snake.direction = 'LEFT'
            if event.key == pygame.K_RIGHT:
                if game.snake.direction != 'LEFT':
                    game.snake.direction = 'RIGHT'
            if event.key == pygame.K_UP:
                if game.snake.direction != 'DOWN':
                    game.snake.direction = 'TOP'
            if event.key == pygame.K_DOWN:
                if game.snake.direction != 'TOP':
                    game.snake.direction = 'DOWN'
            
    
    screen.fill(pygame.Color('white'))
    draw_grid()
    game.draw_elements()
    pygame.display.update()
    timer.tick(60)

