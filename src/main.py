import pygame
from game import DuckHuntGame

def main():
    game = DuckHuntGame(900, 800)
    game.run_main_menu()

if __name__ == "__main__":
    main()