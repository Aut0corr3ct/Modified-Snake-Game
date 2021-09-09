from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 650
SPEED = 75
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOUR = "#00FF00"
FOOD_COLOUR = "#FF0000"
BACKGROUND_COLOUR = "#000000"
POISON_COLOUR = "#FF00FF"

poisons = []

class snake():

    def __init__(self):

        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range (0,BODY_PARTS):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,tag="snake",fill=SNAKE_COLOUR)
            self.squares.append(square)

class Food():


    global poisons
    def __init__(self):

        valid = False
        x = 0
        y = 0

        if len(poisons)>0:
            while valid != True:
                valid = True
                x = random.randint(0, (GAME_WIDTH / SPACE_SIZE - 1)) * SPACE_SIZE
                y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE - 1)) * SPACE_SIZE
                self.coordinates = [x,y]

                for index in (0,len(poisons)-1):
                    if x == poisons[index][0] and y == poisons[index][1]:
                        valid = False
                        break
        else:
            x = random.randint(0, (GAME_WIDTH / SPACE_SIZE - 1)) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE - 1)) * SPACE_SIZE
            self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOUR, tag="food")


class Poison():

    def __init__(self):

        x = random.randint(0,(GAME_WIDTH/SPACE_SIZE-1)) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE - 1)) * SPACE_SIZE

        self.coordinates = [x,y]


        while(self.coordinates==getFoodCoordinates(food)):
            x = random.randint(0, (GAME_WIDTH / SPACE_SIZE - 1)) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE - 1)) * SPACE_SIZE
            self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=POISON_COLOUR, tag="poison")



def getFoodCoordinates(food):

    return food.coordinates


def next_turn(snake,food,poison):

    global poisons
    x , y = snake.coordinates[0]

    if direction == "up":
        y-=SPACE_SIZE

    elif direction == "down":
        y+=SPACE_SIZE

    elif direction == "left":
        x-=SPACE_SIZE

    elif direction == "right":
        x+=SPACE_SIZE

    snake.coordinates.insert(0,(x,y))

    square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOUR)

    snake.squares.insert(0,square) # drawing the snake

    if x ==food.coordinates[0] and y == food.coordinates[1]:

        global score
        score+=1

        label.config(text="Score: {}".format(score))
        canvas.delete("food") # deleting old food

        food = Food() # adding a new food
        poison = Poison() # adding another poison block
        poisons.append(poison.coordinates)

    else:

        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1]) # deleting the last square
        del snake.squares[-1]

    if check_collisions(snake,poison):
        game_over()

    else:
        window.after(SPEED, next_turn,snake,food,poison) # calling function again to move

def change_direction(new_direction):

    global direction

    if new_direction=='left'and direction!= 'right':
        direction = new_direction

    elif new_direction=='right'and direction!= 'left':
        direction = new_direction

    elif new_direction=='up'and direction!= 'down':
        direction = new_direction

    elif new_direction=='down'and direction!= 'up':
        direction = new_direction


def check_collisions(snake,poison):

    global poisons
    x, y = snake.coordinates[0]

    if x<0 or x>=GAME_WIDTH:
        # print("Game Over")
        return True

    elif y<0 or y>=GAME_HEIGHT:
        return True

    if x == poison.coordinates[0] and y == poison.coordinates[1]:

        return True

    for index in range (0,len(poisons)):

        if x == poisons[index][0] and y == poisons[index][1]:

            return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,
                       font=("Consolas",70),text="GAME OVER", fill="red",tag='game over')

window = Tk()
window.title("Snake Game")
window.wm_resizable(False,False)

score = 0
direction = 'down'

label = Label(window,text="Score: {}".format(score),font=("Consolas",40))
label.pack()

canvas = Canvas(window,bg=BACKGROUND_COLOUR,height=GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>',lambda event: change_direction('left'))
window.bind('<Right>',lambda event: change_direction('right'))
window.bind('<Up>',lambda event: change_direction('up'))
window.bind('<Down>',lambda event: change_direction('down'))

snake = snake()
food = Food()
poison = Poison()

next_turn(snake,food,poison)

window.mainloop()