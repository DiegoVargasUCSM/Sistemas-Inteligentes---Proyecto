import sys
import pygame
from src.game import Game


def main():
    game = Game(rows=4, cols=4)
    game.run()


if __name__ == "__main__":
    main()
