#!/usr/bin/env python3
"""
Aventura_textual.py — Juego de texto en Python
"""

import json
import random
import os
import sys
import time

# ---------------------- UTILIDADES ----------------------

def slowprint(text, delay=0.02):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def ask(prompt, options=None):
    while True:
        choice = input(prompt).strip()
        if not options or choice.lower() in options:
            return choice.lower()
        print(f"Opción inválida. Opciones: {', '.join(options)}")

# ---------------------- ESTRUCTURAS ----------------------

DEFAULT_STATE = {
    'player': {
        'name': 'Aventurero',
        'hp': 20,
        'max_hp': 20,
        'attack': 4,
        'gold': 5,
        'inventory': [],
    },
    'location': 'aldea',
    'flags': {},
}

SAVE_FILE = 'aventura_save.json'

# ---------------------- MECÁNICAS ----------------------

def save_game(state):
    with open(SAVE_FILE, 'w') as f:
        json.dump(state, f)
    slowprint('💾 Partida guardada.')

def load_game():
    if not os.path.exists(SAVE_FILE):
        slowprint('No hay partida guardada.')
        return None
    with open(SAVE_FILE, 'r') as f:
        state = json.load(f)
    slowprint('📂 Partida cargada.')
    return state

def show_status(state):
    p = state['player']
    print(f"\n{p['name']} — ❤️ Vida: {p['hp']}/{p['max_hp']}  ⚔️ Ataque: {p['attack']}  💰 Oro: {p['gold']}")
    if p['inventory']:
        print('🎒 Inventario:', ', '.join(p['inventory']))
    else:
        print('🎒 Inventario: (vacío)')

def combat(state, enemy):
    p = state['player']
    slowprint(f"¡Te enfrentas a {enemy['name']}!")
    while p['hp'] > 0 and enemy['hp'] > 0:
        show_status(state)
        print(f"👾 Enemigo: {enemy['name']} — Vida: {enemy['hp']}")
        action = ask('\n¿(a)atacar (u)usar objeto (h)huir? ', options=['a','u','h'])
        if action == 'a':
            dmg = random.randint(1, p['attack'])
            enemy['hp'] -= dmg
            slowprint(f"💥 Le haces {dmg} de daño a {enemy['name']}")
        elif action == 'u':
            if 'poción' in p['inventory']:
                p['inventory'].remove('poción')
                heal = min(p['max_hp'] - p['hp'], 8)
                p['hp'] += heal
                slowprint(f"🍷 Bebes una poción y recuperas {heal} de vida.")
            else:
                slowprint('No tienes objetos utilizables.')
                continue
        else:
            if random.random() < 0.5:
                slowprint('🏃 Escapas con éxito.')
                return 'fled'
            else:
                slowprint('❌ No puedes escapar!')

        if enemy['hp'] > 0:
            edmg = random.randint(1, enemy['atk'])
            p['hp'] -= edmg
            slowprint(f"{enemy['name']} te golpea y te hace {edmg} de daño.")

    if p['hp'] <= 0:
        slowprint('☠️ Has sido derrotado...')
        return 'dead'
    else:
        slowprint(f"🎉 Has vencido a {enemy['name']}!")
        gold = random.randint(2, 6)
        p['gold'] += gold
        slowprint(f"Obtienes {gold} de oro.")
        return 'won'

# ---------------------- ESCENAS ----------------------

def escena_posada(state):
    clear()
    slowprint('🏠 Entras a la posada. La dueña te saluda con una sonrisa cansada.')
    while True:
        print('\nOpciones:')
        print('1) Comprar poción (5 oro)')
        print('2) Dormir (restaura vida por 2 oro)')
        print('3) Volver')
        choice = ask('Elige 1-3: ', options=['1','2','3'])
        if choice == '1':
            if state['player']['gold'] >= 5:
                state['player']['gold'] -= 5
                state['player']['inventory'].append('poción')
                slowprint('Compraste una poción.')
            else:
                slowprint('No tienes suficiente oro.')
        elif choice == '2':
            if state['player']['gold'] >= 2:
                state['player']['gold'] -= 2
                state['player']['hp'] = state['player']['max_hp']
                slowprint('💤 Duermes y recuperas toda tu vida.')
            else:
                slowprint('No tienes suficiente oro.')
        elif choice == '3':
            return

def escena_bosque(state):
    clear()
    slowprint('🌲 Entras al bosque. Los pájaros cantan y el sol se filtra entre las hojas.')
    event = random.choice(['enemigo','tesoro','nada'])
    if event == 'enemigo':
        enemy = {'name': 'Lobo salvaje', 'hp': random.randint(6,10), 'atk': 3}
        result = combat(state, enemy)
        if result == 'dead':
            return 'dead'
    elif event == 'tesoro':
        oro = random.randint(3,8)
        state['player']['gold'] += oro
        slowprint(f'💰 Encuentras una bolsa con {oro} de oro escondida entre las raíces.')
    else:
        slowprint('Caminas un rato sin encontrar nada interesante.')
    ask('\nPresiona Enter para volver a la aldea.')
    state['location'] = 'aldea'

def escena_cueva(state):
    clear()
    slowprint('🕳️ Entras a una cueva oscura. Un eco profundo te pone la piel de gallina.')
    if not state['flags'].get('cueva_boss'):
        slowprint('De pronto, un rugido resuena...')
        boss = {'name': 'Troll de la Cueva', 'hp': 20, 'atk': 5}
        result = combat(state, boss)
        if result == 'dead':
            return 'dead'
        elif result == 'won':
            slowprint('El troll cae con estrépito, dejando tras de sí un cofre brillante.')
            state['player']['inventory'].append('gema mágica')
            state['flags']['cueva_boss'] = True
    else:
        slowprint('La cueva está silenciosa; el troll yace derrotado.')
        if 'gema mágica' in state['player']['inventory']:
            slowprint('Brillas con la luz de la gema... una sensación de poder te invade.')
    ask('\nPresiona Enter para volver a la aldea.')
    state['location'] = 'aldea'

def escena_aldea(state):
    clear()
    slowprint('🏡 Estás en la aldea de Riscos. El olor a pan recién hecho flota en el aire.')
    if not state['flags'].get('intro_met'):
        slowprint('Un anciano te entrega un mapa arrugado: "Cuidado fuera de la aldea", te advierte.')
        state['flags']['intro_met'] = True

    while True:
        show_status(state)
        print('\nOpciones:')
        print('1) Ir al bosque')
        print('2) Entrar a la posada')
        print('3) Ir a la cueva')
        print('4) Guardar partida')
        print('5) Salir del juego')
        choice = ask('\nElige 1-5: ', options=['1','2','3','4','5'])
        if choice == '1':
            state['location'] = 'bosque'
            return
        elif choice == '2':
            escena_posada(state)
        elif choice == '3':
            state['location'] = 'cueva'
            return
        elif choice == '4':
            save_game(state)
        elif choice == '5':
            slowprint('👋 Adiós, viajero.')
            sys.exit(0)

# ---------------------- MAIN LOOP ----------------------

def main():
    clear()
    slowprint('✨ Bienvenido a la Aventura Textual ✨')
    if os.path.exists(SAVE_FILE):
        choice = ask('¿Quieres cargar la partida? (s/n): ', options=['s','n'])
        if choice == 's':
            state = load_game() or DEFAULT_STATE.copy()
        else:
            state = DEFAULT_STATE.copy()
    else:
        state = DEFAULT_STATE.copy()
    p = state['player']
    p['name'] = input('Tu nombre de aventurero: ') or p['name']

    while True:
        loc = state['location']
        if loc == 'aldea':
            escena_aldea(state)
        elif loc == 'bosque':
            if escena_bosque(state) == 'dead':
                break
        elif loc == 'cueva':
            if escena_cueva(state) == 'dead':
                break

    slowprint('💀 Tu aventura termina aquí...')
    if ask('¿Quieres reiniciar? (s/n): ', options=['s','n']) == 's':
        main()
    else:
        slowprint('Gracias por jugar.')

# ---------------------- EJECUCIÓN ----------------------

if __name__ == '__main__':
    main()

# Never gonna give you up