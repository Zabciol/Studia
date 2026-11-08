g = [
    {"id": 1, "maxWeight": None, "space": 20, "allocations": []},
    {"id": 2, "maxWeight": 5, "space": 20, "allocations": []},
    {"id": 3, "maxWeight": 10, "space": 20, "allocations": []},
]

while True:
    try:
        plateNumber = input("Podaj numer rejestracyjny: ")
        weight = float(input("Waga samochodu (w tonach): "))
    except ValueError:
        print("Podaj liczbę.")
        continue

    for level in g:
        fits = level["maxWeight"] is None or weight <= level["maxWeight"]
        if fits and level["space"] - len(level["allocations"]) > 0:
            level["allocations"].append({"plateNumber": plateNumber, "weight": weight})
            print(f"Wjazd na poziom {level['id']}, wolne miejsca: {level['space'] - len(level['allocations'])}")
            break
    else:
        print("Brak miejsca dla tego samochodu.")