import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color(255, 255, 255)
FONT = pygame.font.Font(None, 80)


# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]


# index 0 - 6 represent shape


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        self.active = True
        self.color = COLOR_ACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

    def return_text(self):
        if self.text == '':
            self.text = "NONAME"
        return self.text


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]  # [[(0,0,0). (0,0,0)],[(0,0,0). (0,0,0)]]
    # sets all positions that have blocks in them
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]  # returns 0-3
    # get the positions of the blocks in a piece
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    # offset the position
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


# checks if a space is free
def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)]for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*block_size), (sx+play_width, sy + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy), (sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):
    inc = False
    ind = []
    total_lines = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc = True
            ind.append(i)  # Used to indexing which row had been removed
            total_lines += 1
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            increment = 0
            for d in ind:
                if y < d:
                    increment += 1
            if (increment) > 0:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)

    return total_lines


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Piece', 1, (255, 255, 255))

    # location of next piece
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
                pygame.draw.rect(surface, (128, 128, 128), (int(sx + j * 30), int(sy + i * 30), 30, 30), 1)
    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface, grid, score = 0, level = 1, lines_cleared = 0):
    surface.fill((0, 0, 0))
    # Tetris Title
    font = pygame.font.SysFont('comics', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # score text
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 10, sy - 160))

    # level text
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Level: ' + str(level), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 10, sy - 220))

    # lines cleared text
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Lines Cleared: ' + str(lines_cleared), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 10, sy - 190))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    draw_grid(surface, grid)


def update_score(nscore):

    with open('scores.txt', 'a') as f:
        f.write(str(nscore))
        f.write("\n")



def main(win):
    global grid

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.25
    level = 1
    line_count = 0
    score = 0
    level_increase = False
    pressed_down = False
    pressed_left = False
    pressed_right = False
    move_delay = 0
    lv_up_count = 0

    while run:
        # update grid/game state
        grid = create_grid(locked_positions)
        # timer
        fall_time += clock.get_rawtime()

        # increases level
        if level_increase:
            level += 1
            level_increase = False
            if fall_speed > 0.12 and level <= 19:
                fall_speed -= 0.005
            elif level >= 29:
                fall_speed = 0.075

        # keeps consistent fall rate
        if fall_time/1000 > fall_speed:
            current_piece.y += 1
            move_delay += 1
            if not(valid_space(current_piece,grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if move_delay >= 1:
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1
                        pressed_left = True

                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1
                        pressed_right = True

                    elif event.key == pygame.K_UP or event.key == pygame.K_z:
                        current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                        if not valid_space(current_piece, grid):
                            current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                    elif event.key == pygame.K_x:
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                        if current_piece.rotation < 0:
                            current_piece.rotation = len(current_piece.shape)-1
                        if not valid_space(current_piece, grid):
                            current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)


                    if event.key == pygame.K_DOWN:
                        # move shape down
                        current_piece.y += 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.y -= 1
                        pressed_down = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        pressed_left = False

                    elif event.key == pygame.K_RIGHT:
                        pressed_right = False

                    elif event.key == pygame.K_DOWN:
                        pressed_down = False
            else:
                pressed_left = pressed_right = pressed_down = False

        if fall_time/1000 > fall_speed:
            fall_time = 0
            if pressed_left:
                current_piece.x -= 1
                if not valid_space(current_piece, grid):
                    current_piece.x += 1

            if pressed_right:
                current_piece.x += 1
                if not valid_space(current_piece, grid):
                    current_piece.x -= 1

            if pressed_down:
                # move shape down
                current_piece.y += 1
                if not (valid_space(current_piece, grid)):
                    current_piece.y -= 1
                score += 1
        clock.tick()
        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            # stops blocks appearing out of the grid
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            move_delay = 0
            for pos in shape_pos:
                p = (pos[0], pos[1])
                # piece is locked in
                locked_positions[p] = current_piece.color
            # get new piece
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            # count the number of lines cleared
            lines_cleared = clear_rows(grid, locked_positions)
            # if a number of lines have been cleared
            if lines_cleared > 0:
                score += (10 * lines_cleared) * level
                # if a multiple of 10 is reached
                lv_up_count += lines_cleared
                if lv_up_count >= 10:
                    level_increase = True
                    lv_up_count = 0
            line_count += lines_cleared

        draw_window(win, grid, score, level, line_count)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        # check if game has been lost
        if check_lost(locked_positions):
            draw_text_middle("Game Over", 80, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(1500)
            enter_score(win, score)
            run = False


def enter_score(win, score):
    run = True
    input_box = InputBox(top_left_x + play_width/2 - 100, top_left_y + play_height/2+20, 140, 100)
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Enter your name', 80, (255, 255, 255), win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name = input_box.return_text()
                    game_result = name + "," + str(score)
                    update_score(game_result)
                    run = False
            input_box.handle_event(event)
        input_box.draw(win)
        pygame.display.update()


def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press Any Key to Play', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game

