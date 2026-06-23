Feature: Juego de Memoria
  Como jugador
  Quiero emparejar pares de cartas
  Para poder probar mi memoria

  Scenario: El jugador inicia un juego nuevo
    Given inicio un juego de memoria con tablero de 4x4
    Then deberia ver 16 cartas boca abajo
    And mi puntaje debe mostrar "Pares: 0/8 - Intentos: 0"

  Scenario: El jugador descubre una carta
    Given inicio un juego de memoria con tablero de 4x4
    When descubro la carta en posicion (0, 0)
    Then esa carta debe estar boca arriba

  Scenario: El jugador encuentra un par
    Given inicio un juego de memoria con tablero de 4x4
    When descubro dos cartas con el mismo simbolo
    Then ambas cartas deben quedar boca arriba
    And mis pares encontrados deben aumentar en 1
    And mis intentos deben aumentar en 1

  Scenario: El jugador no encuentra un par
    Given inicio un juego de memoria con tablero de 4x4
    When descubro dos cartas con simbolos diferentes
    Then ambas cartas deben voltearse boca abajo
    And mis intentos deben aumentar en 1

  Scenario: El jugador gana el juego
    Given inicio un juego de memoria con tablero de 2x2
    When emparejo todos los pares
    Then debo ser declarado ganador
    And el juego debe mostrar un mensaje de victoria

  Scenario: El jugador no puede descubrir una carta ya emparejada
    Given inicio un juego de memoria con tablero de 4x4
    When descubro dos cartas con el mismo simbolo
    And intento descubrir una de esas cartas emparejadas de nuevo
    Then la carta no debe cambiar su estado

  Scenario: El jugador pausa el juego
    Given inicio un juego de memoria con tablero de 4x4
    When presiono la tecla de pausa
    Then el juego debe estar en pausa
    And las cartas no deben ser interactuables

  Scenario: El jugador ve las instrucciones
    Given estoy en la pantalla de inicio
    Then deberia ver el titulo "Juego de Memoria"
    And deberia ver instrucciones de como jugar
    And deberia ver un mensaje para iniciar el juego

  Scenario: El jugador pierde por tiempo
    Given inicio un juego de memoria con tablero de 4x4
    And el tiempo se agota
    Then el juego debe mostrar pantalla de tiempo agotado
    And el jugador no debe ser declarado ganador
