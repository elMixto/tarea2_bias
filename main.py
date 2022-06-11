from cmath import sqrt
from dataclasses import dataclass
import csv
import codecs
from operator import index
from matplotlib import pyplot as plt
import pickle
from names_dataset import NameDataset,NameWrapper
from typing import List
import numpy as np

class Point:
    def __init__(self,año,nombre,sexo,frecuencia,proportion,):
        self.año = int(año)
        self.nombre = str(nombre)
        self.sexo = str(sexo)
        self.frecuencia = int(frecuencia)
        self.proportion = float(proportion)

    def __str__(self) -> str:
        return f"Point({self.año},{self.nombre},{self.sexo},{self.frecuencia},{self.proportion})"

#file =codecs.open('nombres.csv',encoding='iso-8859-15')
#reader = csv.reader(file)
#next(reader)
#counter = -1
#data = [Point(*i) for i in reader]
#pickle.dump(data,data_file)

data_file = open("data.bin","rb")
data: List[Point] = pickle.load(data_file)
nombres = set([d.nombre for d in data])

#Que tan comun es mi nombre:
##Una forma de abordarlo sería observar la proporción historica de mi nombre.
jose = [n for n in data if "José" == n.nombre and n.sexo == "M"]

#Grafico el uso historico de José
fig = plt.figure(0)
plt.title("José Over the Years")
plt.xlabel("Year")
plt.ylabel("Proportion %")
plt.plot([j.año for j in jose],[j.proportion*100 for j in jose])
plt.savefig("jose_over_time.png")

#Obtengo mi proporcion final e inicial
p_inicial , p_final = [d.proportion*100 for d in data if d.nombre == "José" and (d.año == 2021 or d.año == 1920)]
print(f"Proporcion_final = {p_final}")
print(f"Proporcion_inicial = {p_inicial}")

#Obtengo el numero total de nombres que se han dado
#y lo comparo con el numero total de frecuncias 
#historicas de mi nombre

toda_fecuencia = sum([d.frecuencia for d in data])
frecuencia_jose = sum([d.frecuencia for d in data if  d.nombre == "José"])
print(f"Todas las frecuencias: {toda_fecuencia}")
print(f"Frecuencia José: {frecuencia_jose}")
print(f"Diferencia: {toda_fecuencia-frecuencia_jose}")
print(f"Proporcion total: {frecuencia_jose/toda_fecuencia}")

###Los beatles afectaron cosillas
beatles_0 = ["John Lennon","Paul McCartney","George Harrison","Ringo Starr"]
beatles = [n.split(" ")[0] for n in beatles_0]
beatles += [n.split(" ")[1] for n in beatles_0]

#Graficamos el registro historico de los beatles
#por separado
del(fig)
fig,ax = plt.subplots()
plt.title("Beatles name proportion over time")
plt.xlabel("Year")
plt.ylabel("Proportion %")
lines = []
for i,b in enumerate(beatles):
    history = [n for n in data if b == n.nombre and n.sexo == "M"]
    x = [h.año for h in history]
    y = [h.proportion*100 for h in history]
    line, = ax.plot(x,y,label=b)
    lines.append(line)
ax.legend(handles=lines, loc="upper left")
plt.savefig("individual_beatles.png")

beatles_0 = ["John Lennon","Paul McCartney","George Harrison","Ringo Starr"]
beatles = [n.split(" ")[0] for n in beatles_0]

años = {}

#Si comparamos con Otros nombres populares en Reino Unido
#fig = plt.figure(2)
#plt.title("Beatles vs other common United Kindom names")
#plt.xlabel("Year")
#plt.ylabel("Proportion %")
#nd = NameDataset()
#nombre_pais = dict()
#for n in nombres:
#    pais = NameWrapper(nd.search(n)).country 
#    if pais not in nombre_pais:
#        nombre_pais[pais] = []
#    nombre_pais[pais].append(n)
#
#britains = nombre_pais['United Kingdom']
#
#for b in list(set(britains+beatles)):
#    nombre = [n for n in data if b  == n.nombre and n.sexo == "M"]
#    if len(nombre) == 0:
#        continue
#    x = [d.año for d in nombre]
#    y = [d.proportion*100 for d in nombre]
#    if b in beatles:
#        plt.plot(x,y,color="red")
#    elif y[-1] > 0.1:
#        continue
#    else:
#        plt.plot(x,y,color="blue")
#plt.savefig("beatles_constrat.png")


#Gender distribution
x = []
del(fig)
fig,ax = plt.subplots()
years = [y for y in range(1921,2022)]
men_1920 = sum([d.proportion*100 for d in data if d.año == 1920 and d.sexo == "M"])
women_1920 = sum([d.proportion*100 for d in data if d.año == 1920 and d.sexo == "F"])
print(men_1920,women_1920)
men = [sum([d.proportion*100 for d in data if d.año == y and d.sexo == "M"]) for y in years]
women = [sum([d.proportion*100 for d in data if d.año == y and d.sexo == "F"]) for y in years]
I = [sum([d.proportion*100 for d in data if d.año == y and d.sexo == "I"]) for y in years]

men_average = sum(men)/len(men)
men_std = sqrt(sum([(i-men_average)**2 for i in men])/len(men))
men_var = men_std**2

women_average = sum(women)/len(women)
women_std = sqrt(sum([(i-women_average)**2 for i in women])/len(women))
women_var = men_std**2

I_average = sum(I)/len(I)
I_std = sqrt(sum([(i-I_average)**2 for i in I])/len(I))
I_var = I_std**2

print(f"var(men): {men_var}")
print(f"std(men): {men_std}")
print(f"max(men): {max(men)}")
print(f"min(men): {min(men)}")

print(f"var(I): {I_var}")
print(f"std(I): {I_std}")
print(f"max(I): {max(I)}")
print(f"min(I): {min(I)}")

print(f"var(women): {women_var}")
print(f"std(women): {women_std}")
print(f"max(women): {max(women)}")
print(f"min(women): {min(women)}")

print(f"Men proportion 1920: {men_1920} ")
print(f"Women proportion 1920: {women_1920} ")
print(f"Average men proportion: {men_average}")
print(f"Average women proportion: {women_average}")
print(f"Average I proportion: {I_average}")
confidence_interval = ()

ax.stackplot(years, men,women,labels=['Masculino','Femenino'])
#ax.stackplot(years, women, bottom=men,label='Femenino')
plt.xlabel("Years")
plt.ylabel("Proportion %")
plt.savefig("gender_distribution.png")
fig = plt.figure(4)
I = [sum([d.frecuencia for d in data if d.año == y and d.sexo == "I"]) for y in years]
plt.plot(years[84:],I[84:])
plt.savefig("I_evolution")
#Sexo indeterminado
#Agreg