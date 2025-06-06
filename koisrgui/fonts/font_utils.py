# koisrgui/fonts/font_utils.py
import pygame
import os

def load_font(font_name, size):
    return pygame.font.SysFont(font_name, size)
