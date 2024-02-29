
"""
Main module for starting the Duck Hunt game.
"""
from game import DuckHuntGame


def main():
    """
    Main function to start the Duck Hunt game.
    """
    game = DuckHuntGame(900, 800)
    game.run_main_menu()


if __name__ == "__main__":
    main()
