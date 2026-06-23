import pytest
from src.board import Board
from src.player import Player
from src.card import Card


class TestAcceptanceFunctionalRequirements:
    """ATDD: Validación de requisitos funcionales desde el punto de vista del usuario."""

    def test_user_can_start_game(self):
        board = Board(4, 4)
        assert len(board.cards) == 16
        assert all(not c.is_revealed for c in board.cards)

    def test_user_can_reveal_card_by_clicking(self):
        board = Board(4, 4)
        card = board.select_card(0, 0)
        assert card.is_revealed is True

    def test_user_cannot_reveal_matched_card(self):
        board = Board(4, 4)
        card1 = board.select_card(0, 0)
        card1.match()
        was_revealed = card1.is_revealed
        board.select_card(0, 0)
        assert card1.is_matched is True
        assert card1.is_revealed == was_revealed

    def test_user_sees_feedback_on_match(self):
        board = Board(4, 4)
        card1 = board.select_card(0, 0)
        target_symbol = card1.symbol
        for c in board.cards:
            if c.symbol == target_symbol and c.id != card1.id:
                board.select_card(c.position[0], c.position[1])
                break
        assert board.check_match() is True
        assert card1.is_matched is True

    def test_user_sees_feedback_on_mismatch(self):
        board = Board(4, 4)
        card1 = board.select_card(0, 0)
        for c in board.cards:
            if c.symbol != card1.symbol and not c.is_revealed:
                board.select_card(c.position[0], c.position[1])
                break
        assert board.check_match() is False

    def test_user_can_complete_game(self):
        board = Board(2, 2)
        player = Player(total_pairs=2)
        for card in board.cards:
            card.match()
            player.add_pair()
        assert board.is_complete() is True
        assert player.is_winner is True

    def test_user_score_tracks_attempts(self):
        player = Player(total_pairs=8)
        assert player.attempts == 0
        player.increment_attempts()
        assert player.attempts == 1

    def test_user_score_tracks_pairs(self):
        player = Player(total_pairs=8)
        assert player.pairs_found == 0
        player.add_pair()
        assert player.pairs_found == 1

    def test_user_can_pause_and_resume(self):
        from src.game import Game
        import pygame
        game = Game(rows=4, cols=4)
        game.state = Game.STATE_PLAYING
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_p})
        game.handle_event(event)
        assert game.state == Game.STATE_PAUSED

    def test_user_can_resume_from_pause(self):
        from src.game import Game
        import pygame
        game = Game(rows=4, cols=4)
        game.state = Game.STATE_PAUSED
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_p})
        game.handle_event(event)
        assert game.state == Game.STATE_PLAYING

    def test_user_sees_start_screen(self):
        from src.game import Game
        game = Game(rows=4, cols=4)
        assert game.state == Game.STATE_START

    def test_user_sees_game_over_screen(self):
        board = Board(2, 2)
        player = Player(total_pairs=2)
        for card in board.cards:
            card.match()
            player.add_pair()
        assert board.is_complete() is True
        assert player.is_winner is True

    def test_user_can_restart_game(self):
        board = Board(4, 4)
        player = Player(total_pairs=8)
        original_cards = board.cards[:]
        board = Board(4, 4)
        player.reset()
        assert player.attempts == 0
        assert player.pairs_found == 0
        assert len(board.cards) == 16

    def test_game_has_time_limit(self):
        from src.game import Game
        game = Game(rows=4, cols=4)
        assert game.TIME_LIMIT == 100

    def test_time_remaining_starts_at_max(self):
        import pygame
        from src.game import Game
        game = Game(rows=4, cols=4)
        game.state = Game.STATE_PLAYING
        game.start_ticks = pygame.time.get_ticks()
        assert game.time_remaining <= 100
        assert game.time_remaining > 95

    def test_game_lost_when_time_expires(self):
        import pygame
        from src.game import Game
        game = Game(rows=4, cols=4)
        game.state = Game.STATE_PLAYING
        game.start_ticks = pygame.time.get_ticks() - 101000
        game.update()
        assert game.state == Game.STATE_LOST

    def test_can_restart_after_losing(self):
        import pygame
        from src.game import Game
        game = Game(rows=4, cols=4)
        game.state = Game.STATE_PLAYING
        game.start_ticks = pygame.time.get_ticks() - 101000
        game.update()
        assert game.state == Game.STATE_LOST
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        game.handle_event(event)
        assert game.state == Game.STATE_PLAYING
        assert game.time_remaining > 95
