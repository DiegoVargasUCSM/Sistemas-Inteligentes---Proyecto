import pytest
import pygame
from src.game import Game


class TestGame:
    def test_penalty_applied_on_mismatch(self):
        game = Game(rows=2, cols=2)
        game.state = Game.STATE_PLAYING
        game.start_ticks = 50000
        before = game.start_ticks
        cards = game.board.cards
        card_a = cards[0]
        card_b = None
        for c in cards:
            if c.symbol != card_a.symbol:
                card_b = c
                break
        game._handle_card_click(card_a.position[0], card_a.position[1])
        game._handle_card_click(card_b.position[0], card_b.position[1])
        assert game.start_ticks == before - 5000

    def test_no_penalty_on_match(self):
        game = Game(rows=2, cols=2)
        game.state = Game.STATE_PLAYING
        game.start_ticks = 50000
        before = game.start_ticks
        cards = game.board.cards
        card_a = cards[0]
        card_b = None
        for c in cards:
            if c.symbol == card_a.symbol and c.id != card_a.id:
                card_b = c
                break
        game._handle_card_click(card_a.position[0], card_a.position[1])
        game._handle_card_click(card_b.position[0], card_b.position[1])
        assert game.start_ticks == before

    def test_penalty_does_not_go_below_zero(self):
        game = Game(rows=2, cols=2)
        game.state = Game.STATE_PLAYING
        game.start_ticks = 1000
        cards = game.board.cards
        card_a = cards[0]
        card_b = None
        for c in cards:
            if c.symbol != card_a.symbol:
                card_b = c
                break
        game._handle_card_click(card_a.position[0], card_a.position[1])
        game._handle_card_click(card_b.position[0], card_b.position[1])
        assert game.start_ticks == 0
