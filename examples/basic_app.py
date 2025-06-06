# examples/basic_app.py
import pygame
from koisrgui.core.manager import GUIManager
from koisrgui.widgets.button import Button
from koisrgui.widgets.label import Label
from koisrgui.themes.dark import DARK_THEME

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
gui = GUIManager(screen)

label = Label(100, 50, 200, 30, "Hello, koisrgui!", style=DARK_THEME)
btn = Button(100, 100, 120, 40, "Click Me", on_click=lambda: print("Clicked!"), style=DARK_THEME)
gui.add_widget(label)
gui.add_widget(btn)

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        gui.handle_event(event)
    gui.update(dt)
    screen.fill(DARK_THEME['bg'])
    gui.draw()
    pygame.display.flip()
pygame.quit()
