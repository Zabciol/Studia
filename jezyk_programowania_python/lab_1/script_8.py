from random import randint

x = int(input('Podaj pierwszą liczbę (1-6): '))
y = int(input('Podaj drugą liczbę (1-6): '))

if not (1 <= x <= 6 and 1 <= y <= 6):
  print('Liczby muszą być z zakresu 1-6')
else:
  los1 = randint(1, 6)
  los2 = randint(1, 6)
  print('Wylosowano: {} i {}'.format(los1, los2))

  trafione = (x == los1) + (y == los2)
  if trafione == 0:
    print('przegrałeś')
  elif trafione == 1:
    print('trafiłeś 1 liczbę')
  else:
    print('trafiłeś 2 liczby')
