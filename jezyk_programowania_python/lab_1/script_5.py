import math

print('Równanie postaci ax^2 + bx + c = 0')
a = float(input('Podaj a: '))
b = float(input('Podaj b: '))
c = float(input('Podaj c: '))

if a == 0:
  print('To nie jest równanie kwadratowe (a = 0)')
else:
  delta = b**2 - 4*a*c
  if delta > 0:
    x1 = (-b - math.sqrt(delta)) / (2*a)
    x2 = (-b + math.sqrt(delta)) / (2*a)
    print('Dwa pierwiastki: x1 = {:.2f}, x2 = {:.2f}'.format(x1, x2))
  elif delta == 0:
    print('Jeden pierwiastek: x0 = {:.2f}'.format(-b / (2*a)))
  else:
    print('Brak pierwiastków rzeczywistych (delta < 0)')
