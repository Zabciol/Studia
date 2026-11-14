import math

a = float(input('Podaj długość boku a: '))
b = float(input('Podaj długość boku b: '))
c = float(input('Podaj długość boku c: '))

if a + b > c and a + c > b and b + c > a and a > 0 and b > 0 and c > 0:
  p = (a + b + c) / 2
  pole = math.sqrt(p * (p - a) * (p - b) * (p - c))  # wzór Herona
  print('Pole trójkąta: {:.2f}'.format(pole))
else:
  print('Z podanych boków nie da się utworzyć trójkąta')
