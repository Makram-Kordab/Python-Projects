from tkinter import *
import random
import time

GAME_WIDTH = 800
GAME_HEIGHT = 600
SPEED = 100
SPACE_SIZE = 40
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
score = 0
direction = 'down'
plays = 0



class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self):

        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def CountDown(sec=3):
    if sec > 0:
        canvas.delete("all")
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                           text=str(sec), font=('Comic Sans MS', 120), fill="red")
        window.after(1000, CountDown, sec - 1)
    elif sec == 0:
        canvas.delete("all")
        StartGame()


def NextTurn(snake, food):

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if CheckCollisions(snake):
        GameOver()

    else:
        window.after(SPEED, NextTurn, snake, food)


def ChangeDirection(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def CheckCollisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def StartGame():
    snake = Snake()
    food = Food()
    NextTurn(snake, food)

def ResetGame():
    global score, direction, snake, food
    
    score = 0
    label.config(text="Score:{}".format(score))
    direction = 'down'
    
    canvas.delete(ALL)
    CountDown(3)

def GameOver():

    global plays    

    canvas.delete(ALL)
    
    tempwidth = canvas.winfo_width()/2
    tempheight = canvas.winfo_height()/2
    
    canvas.create_text(tempwidth, (tempheight)-190, font=('Comic Sans MS',70), text="GAME OVER", fill="red", tag="gameover")
    
    
    PlayAgain = Button(window, text="Play Again", font=('Comic Sans MS', 40), command=ResetGame, bg="gray", fg="red")
    canvas.create_window(tempwidth, tempheight, window=PlayAgain)
    
    if plays == 0:
        plays +=1
        instruction = Label(window, text="Press esc to close the game!\nPress f to enter full screen!")
        instruction.pack(side=BOTTOM)
    

def InGame():
    
    global canvas, label
    
    for widget in window.winfo_children():
        widget.destroy()
    
    label = Label(window, text="Score:{}".format(score), font=('Consolas', 40))
    label.pack()
        
    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()
    
        
    window.update()
    
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))
    
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    window.bind('<Left>', lambda event: ChangeDirection('left'))
    window.bind('<Right>', lambda event: ChangeDirection('right'))
    window.bind('<Up>', lambda event: ChangeDirection('up'))
    window.bind('<Down>', lambda event: ChangeDirection('down'))
    
    CountDown(3)



window = Tk()
window.title("Snake game")
window.resizable(True, True)
window.minsize(GAME_WIDTH, GAME_HEIGHT+110)
window.attributes('-fullscreen',False)
window.bind('<Escape>', lambda event: window.destroy())
window.bind('<f>', lambda event: window.attributes('-fullscreen', True))


GameName = Label(window, text="Snake Game", font=('Comic Sans MS',70), fg="red")
GameName.pack(pady=(50,0))

ProducedBy = Label(window, text="produced by Makram Kordab", font=('Arial',20))
ProducedBy.pack()


#here i want to give the users a hint about the game    canvas.winfo_width() / 2
idea = Canvas(window, width=GAME_WIDTH, height=SPACE_SIZE*3)
idea.pack()
idea.update_idletasks()

canvas_width = idea.winfo_width()
canvas_height = idea.winfo_height()

circle_diameter = 40
circle_radius = circle_diameter / 2

bottom_right_x = canvas_width - circle_radius
bottom_right_y = canvas_height - circle_radius

idea.create_oval(GAME_WIDTH/2 +100 , SPACE_SIZE * 3 - 40, GAME_WIDTH/2+140, SPACE_SIZE * 3, fill=FOOD_COLOR)
idea.create_rectangle(GAME_WIDTH/2-60, SPACE_SIZE * 3 - 40, GAME_WIDTH/2-20, SPACE_SIZE * 3, fill=SNAKE_COLOR)
idea.create_rectangle(GAME_WIDTH/2-100, SPACE_SIZE * 3 - 40, GAME_WIDTH/2-60, SPACE_SIZE * 3, fill=SNAKE_COLOR)
idea.create_rectangle(GAME_WIDTH/2-140, SPACE_SIZE * 3 - 40, GAME_WIDTH/2-100, SPACE_SIZE * 3, fill=SNAKE_COLOR)



instructions = Label(window, text="Press esc to close the game!\nPress f to enter full screen!")
instructions.pack(side=BOTTOM)

PlayNow = Button(window, text="Play Now", font=('Comic Sans MS', 40), command=InGame, bg="black", fg="red", activebackground="gray", activeforeground="white")
PlayNow.pack(side=BOTTOM, pady=(0,50))

window.mainloop()