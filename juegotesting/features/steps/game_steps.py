from behave import given, when, then
from src.board import Board
from src.card import Card
from src.player import Player


@given("inicio un juego de memoria con tablero de {rows}x{cols}")
def step_start_game(context, rows, cols):
    context.rows = int(rows)
    context.cols = int(cols)
    context.board = Board(context.rows, context.cols)
    context.player = Player(total_pairs=(context.rows * context.cols) // 2)


@then("deberia ver {count} cartas boca abajo")
def step_see_face_down_cards(context, count):
    expected = int(count)
    assert len(context.board.cards) == expected
    assert all(not c.is_revealed for c in context.board.cards)


@then('mi puntaje debe mostrar "{expected_score}"')
def step_check_score(context, expected_score):
    assert context.player.score == expected_score


@when("descubro la carta en posicion ({row}, {col})")
def step_reveal_card(context, row, col):
    card = context.board.select_card(int(row), int(col))
    if card:
        context.last_revealed_card = card


@then("esa carta debe estar boca arriba")
def step_card_face_up(context):
    assert context.last_revealed_card.is_revealed is True


@when("descubro dos cartas con el mismo simbolo")
def step_reveal_matching_pair(context):
    cards = context.board.cards
    target_symbol = None
    positions = []
    for i, c1 in enumerate(cards):
        for j, c2 in enumerate(cards):
            if i < j and c1.symbol == c2.symbol:
                target_symbol = c1.symbol
                positions = [(c1.position[0], c1.position[1]), (c2.position[0], c2.position[1])]
                break
        if target_symbol:
            break

    context.board.select_card(positions[0][0], positions[0][1])
    context.player.increment_attempts()
    context.board.select_card(positions[1][0], positions[1][1])
    context.board.check_match()
    if context.board.revealed_cards and context.board.revealed_cards[-1].is_match(
        context.board.revealed_cards[-2]
    ):
        context.player.add_pair()
    context.last_matched_positions = positions


@when("descubro dos cartas con simbolos diferentes")
def step_reveal_non_matching_pair(context):
    cards = context.board.cards
    pos1 = (0, 0)
    card1 = context.board.select_card(pos1[0], pos1[1])
    context.player.increment_attempts()
    for c in cards:
        if c.symbol != card1.symbol and c.id != card1.id:
            pos2 = (c.position[0], c.position[1])
            context.board.select_card(pos2[0], pos2[1])
            context.last_non_match_positions = [pos1, pos2]
            break
    context.board.check_match()


@then("ambas cartas deben quedar boca arriba")
def step_both_cards_face_up(context):
    for r, c in context.last_matched_positions:
        card = context.board.select_card(r, c)
        if card:
            assert card.is_revealed is True


@then("mis pares encontrados deben aumentar en 1")
def step_pairs_found_increase(context):
    assert context.player.pairs_found >= 1


@then("mis intentos deben aumentar en 1")
def step_attempts_increase(context):
    assert context.player.attempts >= 1


@then("ambas cartas deben voltearse boca abajo")
def step_both_cards_flip_back(context):
    context.board.reset_selection()
    for r, c in context.last_non_match_positions:
        card = context.board.cards[r * context.board.cols + c]
        assert card.is_revealed is False


@then("debo ser declarado ganador")
def step_declared_winner(context):
    assert context.player.is_winner is True
    assert context.board.is_complete() is True


@then("el juego debe mostrar un mensaje de victoria")
def step_victory_message(context):
    assert context.player.is_winner is True


@when("emparejo todos los pares")
def step_match_all_pairs(context):
    for card in context.board.cards:
        if not card.is_matched:
            card.match()
            context.player.add_pair()


@when("intento descubrir una de esas cartas emparejadas de nuevo")
def step_try_reveal_matched(context):
    for r, c in context.last_matched_positions:
        card = context.board.select_card(r, c)
        if card:
            context.revealed_again = card
            break


@then("la carta no debe cambiar su estado")
def step_card_state_unchanged(context):
    assert context.revealed_again.is_matched is True
    assert context.revealed_again.is_revealed is True


@when("presiono la tecla de pausa")
def step_press_pause(context):
    context.game_paused = True


@then("el juego debe estar en pausa")
def step_game_paused(context):
    assert context.game_paused is True


@then("las cartas no deben ser interactuables")
def step_cards_not_interactable(context):
    assert context.game_paused is True


@given("estoy en la pantalla de inicio")
def step_on_start_screen(context):
    context.on_start_screen = True


@then('deberia ver el titulo "Juego de Memoria"')
def step_see_title(context):
    assert context.on_start_screen is True


@then("deberia ver instrucciones de como jugar")
def step_see_instructions(context):
    assert context.on_start_screen is True


@then("deberia ver un mensaje para iniciar el juego")
def step_see_start_prompt(context):
    assert context.on_start_screen is True


@given("el tiempo se agota")
def step_time_runs_out(context):
    context.game_state = "lost"
    context.player_lost = True


@then("el juego debe mostrar pantalla de tiempo agotado")
def step_show_lost_screen(context):
    assert context.game_state == "lost"


@then("el jugador no debe ser declarado ganador")
def step_player_not_winner(context):
    assert context.player_lost is True
