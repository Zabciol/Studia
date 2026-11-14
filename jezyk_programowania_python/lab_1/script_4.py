# Schemat: Sejm od 21 lat, Senat od 30 lat, Prezydent od 35 lat
wiek = int(input('Podaj wiek kandydata: '))

if wiek < 18:
  print('Jesteś niepełnoletni i nie możesz zostać prezeydentem')
elif wiek < 35:
  print('Jesteś pełnoletni ale nie możesz zostać prezeydentem')
else:
  print('Jesteś pełnoletni i możesz zostać prezeydentem')
