import pygame
import math
import random
import tkinter
from tkinter import font


pygame.init()

screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
wheel = pygame.Surface((600, 600), pygame.SRCALPHA)
clock = pygame.time.Clock()

font1 = pygame.font.Font('bin/arialbd.ttf', 25)

angle = 0
angleChange = 0
currentAngle = 90
colors = [(240, 180, 20), (0, 150, 40), (51, 105, 230), (215, 15, 40), (250, 105, 0)]
first = True
final = False
removed = True
text = font1.render('', True, (220, 220, 220))
spinText = font1.render('Spin', True, (220, 220, 220))
removeText = font1.render('Remove', True, (220, 220, 220))
configText = font1.render('Config', True, (220, 220, 220))
picked = ''

# items = ['Name1', 'Name2', 'Name3', 'Name3', 'Name3', 'Name3', 'Name3', 'Name3', 'Name3', 'Name3', 'Name3', 'Name3', 'Name3', 'Name3', 'Name3', 'Name3', 'Name3']
items = []
with open('bin/config.txt', 'r') as f:
    for i in f.readlines():
        items.append(i.replace('\n', ''))

if items:
    deg = 360 / len(items)

random.shuffle(colors)
random.shuffle(items)


def save():
    items.clear()
    temp = ''
    for i in textBox.get('1.0', 'end').split('\n'):
        if i != '':
            items.append(i)
            temp += i + '\n'

    with open('bin/config.txt', 'w') as f:
        f.write(temp)

    if len(items) > 1:
        random.shuffle(items)
        makeWheel()

    global first, removed, picked, text

    first = True
    removed = True
    picked = ''
    text = font1.render('', True, (220, 220, 220))


def close():
    global openConf
    openConf = False
    window.destroy()


# Any point (x,y) on the path of the circle is x=r∗sin(θ),y=r∗cos(θ)

def makeWheel():
    c = 0
    deg = 360 / len(items)

    for i in range(len(items)):
        a = 300 + 290 * math.sin(deg * i * math.pi / 180)
        b = 300 + 290 * math.cos(deg * i * math.pi / 180)
        a2 = 300 + 290 * math.sin(deg * (i + 1) * math.pi / 180)
        b2 = 300 + 290 * math.cos(deg * (i + 1) * math.pi / 180)

        if len(items) > 3:
            pygame.draw.polygon(wheel, colors[c], ((a, b), (a2, b2), (300, 300)))
        else:
            a3 = 300 + 290 * math.sin((deg * i + deg * (i + 1)) / 2 * math.pi / 180)
            b3 = 300 + 290 * math.cos((deg * i + deg * (i + 1)) / 2 * math.pi / 180)
            pygame.draw.polygon(wheel, colors[c], ((a, b), (a3, b3), (a2, b2), (300, 300)))

        c = 0 if c == len(colors) - 1 else c + 1

    for i in range(len(items)):
        newItem = items[i][:15]
        item = font1.render(' ' * (45 - len(newItem)) + newItem, True, (220, 220, 220))
        item = pygame.transform.flip(item, 1, 1)

        rotatedItem = pygame.transform.rotate(item, (deg * i + deg * (i + 1)) / 2 + 90)
        rotatedItem_rect = rotatedItem.get_rect(center=(300, 300))

        wheel.blit(rotatedItem, rotatedItem_rect)


if items:
    makeWheel()

openConf = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not final and angleChange == 0:
            pos = pygame.mouse.get_pos()
            if len(items) > 1 and spinButton.collidepoint(pos):
                angleChange = random.randrange(40, 55)
                picked = ''
                first = False
                removed = False
                deg = 360 / len(items)
            elif picked and removeButton.collidepoint(pos):
                removed = True
                items.remove(picked)
                deg = 360 / len(items)
                wheel.fill((0, 0, 0))
                makeWheel()
            elif configButton.collidepoint(pos) and not openConf:
                openConf = True
                window = tkinter.Tk()
                window.title('Wheel Config')
                window.geometry('500x500')
                window.protocol("WM_DELETE_WINDOW", close)

                font2 = tkinter.font.Font(family='bin/arialbd.tff', size=16)
                textBox = tkinter.Text(window, height=25, width=60)
                textBox.pack(expand=False)

                button1 = tkinter.Button(text="Save", width=10, height=1, bg="white", fg="black", font=font2, command=save)
                button1.place(x=100, y=450)
                button2 = tkinter.Button(text="Close", width=10, height=1, bg="white", fg="black", font=font2, command=close)
                button2.place(x=250, y=450)

                textBox.delete(1.0, "end")
                with open('bin/config.txt', 'r') as f:
                    for i in f.readlines():
                        textBox.insert('end', i)

    screen.fill((0, 0, 0))

    if openConf:
        window.update()

    if angleChange <= 0 and not picked and not first:
        angleChange = 0

        for i in range(len(items)):
            if (i + 1) * deg >= currentAngle % 360 >= i * deg:
                text = font1.render(items[i], True, (220, 220, 220))
                picked = items[i]

    angle += angleChange
    currentAngle += angleChange

    if angleChange > 0:
        angleChange -= .5

    rotatedWheel = pygame.transform.rotate(wheel, -angle)
    rotatedWheel_rect = rotatedWheel.get_rect(center=(300, 300))
    screen.blit(rotatedWheel, rotatedWheel_rect)

    pygame.draw.ellipse(screen, (0, 0, 0), (-200, -200, 1000, 1000), 300)
    pygame.draw.polygon(screen, (0, 0, 0), ((360, 300), (300, 275), (300, 325)))
    pygame.draw.polygon(screen, (255, 0, 0), ((350, 300), (300, 280), (300, 320)))
    pygame.draw.ellipse(screen, (0, 0, 0), (275, 275, 50, 50))

    final = picked and len(items) == 2 and not removed

    if not final:
        if picked and not removed:
            spinButton = pygame.draw.rect(screen, (60, 60, 60), (screen.get_width() / 2 - 100 - 125, 520, 200, 70), 2)
            removeButton = pygame.draw.rect(screen, (60, 60, 60), (screen.get_width() / 2 - 100 + 125, 520, 200, 70), 2)
            screen.blit(removeText, (removeButton.x + removeButton.width / 2 - removeText.get_width() / 2, removeButton.y + removeButton.height / 2 - removeText.get_height() / 2))
            screen.blit(spinText, (spinButton.x + spinButton.width / 2 - spinText.get_width() / 2, spinButton.y + spinButton.height / 2 - spinText.get_height() / 2))

            screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, 40))
        elif angleChange == 0 and removed and len(items) > 1:
            spinButton = pygame.draw.rect(screen, (60, 60, 60), (screen.get_width() / 2 - 100, 520, 200, 70), 2)
            screen.blit(spinText, (spinButton.x + spinButton.width / 2 - spinText.get_width() / 2, spinButton.y + spinButton.height / 2 - spinText.get_height() / 2))

    if angleChange == 0:
        screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, 40))

    configButton = pygame.draw.rect(screen, (60, 60, 60), (10, 10, 100, 50), 2)
    screen.blit(configText, (configButton.x + configButton.width / 2 - configText.get_width() / 2, configButton.y + configButton.height / 2 - configText.get_height() / 2))

    pygame.display.flip()
    clock.tick(50)