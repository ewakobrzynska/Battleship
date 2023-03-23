from main import *
#TWORZENIE STATKÓW
temp = 0
#tworzenie 10 statkow
while temp < 10:
    ship_info = random_location()
    if ship_info == 'None':
        continue
    else:
        ship_list.append(Ship(ship_info['size'], ship_info['orientation'], ship_info['location']))
        temp += 1
    print(ship_info)
    print_board(board)
del temp

#GRA

print_board(board)
#print_board(board_display)
#Wprowadzenie przez gracza wiersza i kolumny
for tura in range(num_turns):
    print("Tura:", tura + 1)
    guess_coords = {}
    while True:
        guess_coords['row'] = get_row()
        guess_coords['col'] = get_col()
        #jesli dane pole bylo juz sprawdzane
        if board_display[guess_coords['row']][guess_coords['col']] == 'X' or board_display[guess_coords['row']][guess_coords['col']] == '*':
            print("\nJuz sprawdzales to pole")
        else:
            break
#Analiza trafienia
    ship_hit = False
    for ship in ship_list:
        #jeśli jest statek na koordynatach wprowadzonych przez gracza
        if ship.contains(guess_coords):
            ship_hit = True #trafiony
            board_display[guess_coords['row']][guess_coords['col']] = 'X' #zaznacz na mapie X (trafiony)
            if ship.destroyed():#jesli zniczszono caly statek
                ship_list.remove(ship)
            break
    if not ship_hit:
        board_display[guess_coords['row']][guess_coords['col']] = '*' #zaznacz na mapie * (sprawdzony)

    print_board(board_display)

    if not ship_list:
        break

#ZAKONCZENIE GRY
if ship_list: #jesli ship_list nie jest pusta (istnieje jakis statek na planszy)
    print("Przegrales")
else:
    print("Wygrales")