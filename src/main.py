import pygame
from src.game import Game

def main():
    game = Game(900, 800)
    game.run_main_menu()

if __name__ == "__main__":
    main()