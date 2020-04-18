# Adaptacion: 29/Mar/2020, por Egner Aceros, egner.aceros@gmail.com, TepuyRDGroup, http://tepuyrd.com/, twitter: @TepuyRDGroup
# Equipo 4: Modelo para predecir la propagación del COVID19

# Referencia 1: Castro P., De los Reyes J. , Gonzalez S., Merino P., Ponce J.,
# "Modelización y Simulación de la propagación del virus sars-cov-2 en Ecuador"
# Centro de Modelización Matemática en Áreas Clave para el Desarrollo, MODEMAT
# Escuela Politécnica Nacional de Ecuador. modemat@epn.edu.ec, 26 de marzo de 2020

# Referencia 2: https://rosettacode.org/wiki/Runge-Kutta_method

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import sys
 
def rk4(f, g, h, x0, y0, z0, t0, tf, beta, gamma, n, hh):
    vt = [0] * (n + 1)
    vx = [0] * (n + 1)
    vy = [0] * (n + 1)
    vz = [0] * (n + 1)
    #hh = 0.01
    vt[0] = t = t0
    vx[0] = x = x0
    vy[0] = y = y0
    vz[0] = z = z0
    i = 0
    while t < tf:
    #for i in range(1, n + 1):
        k1 = hh * f(x, y, z, beta[i], gamma)
        l1 = hh * g(x, y, z, beta[i], gamma)
        m1 = hh * h(x, y, z, beta[i], gamma)
        k2 = hh * f(x + k1/2, y + l1/2, z + m1/2, beta[i], gamma)
        l2 = hh * g(x + k1/2, y + l1/2, z + m1/2, beta[i], gamma)
        m2 = hh * h(x + k1/2, y + l1/2, z + m1/2, beta[i], gamma)
        k3 = hh * f(x + k2/2, y + l2/2, z + m2/2, beta[i], gamma)
        l3 = hh * g(x + k2/2, y + l2/2, z + m2/2, beta[i], gamma)
        m3 = hh * h(x + k2/2, y + l2/2, z + m2/2, beta[i], gamma)
        k4 = hh * f(x + k3, y + l3, z + m3, beta[i], gamma)
        l4 = hh * g(x + k3, y + l3, z + m3, beta[i], gamma)
        m4 = hh * h(x + k3, y + l3, z + m3, beta[i], gamma)
        vt[i] = t = t0 + i * hh
        vx[i] = x = x + (k1 + 2*k2 + 2*k3 + k4) / 6
        vy[i] = y = y + (l1 + 2*l2 + 2*l3 + l4) / 6
        vz[i] = z = z + (m1 + 2*m2 + 2*m3 + m4) / 6
        i = i + 1
    return vt, vx, vy, vz
 
def f(x, y, z, beta, gamma):
    return (-beta*y*x)

def g(x, y, z, beta, gamma):
    return (beta*x - gamma)*y

def h(x, y, z, beta, gamma):
    return (gamma*y)

#Inicio

parser = argparse.ArgumentParser(description='Modelo analítico COVID19 basado en SIR (Susceptibles, Infectados, Removidos)')

#Datos de la simulacion
parser.add_argument('-t0','--tiempo-inicial-sim', help="Tiempo inicial de simulación en días. Si no es especificado se asume 0", required=False, type=int, default=0)
parser.add_argument('-tf','--tiempo-final-sim', help="Tiempo final de simulación en días. Si no es especificado se asume 15 días", required=False, type=int, default=15)
parser.add_argument('-hh','--delta', help="Paso o delta de tiempo (dt). Este parametro es suceptible al método de resolucion. Si no es especificado se asume 0.01 días", required=False, type=float, default=0.01)
#Condiciones iniciales
parser.add_argument('-r0','---infeccion-inicial', help="Fraccion de Infeccion Inicial. Si no es especificado se asume 0.0000045", required=False, type=float, default=0.0000045)
parser.add_argument('-x0','--susceptible-inicial', help="Fraccion Suceptible Inicial. Si no es especificado se asume 1 - r0", required=False, type=float, default=-1)
parser.add_argument('-z0','--removidos-inicial', help="Fraccion de Removidos Inicial. Si no es especificado se asume 0", required=False, type=float, default=0)
#Parametros del modelo
parser.add_argument('-bmx','--betamx', help="Límite máximo del parámetro beta (tasa de transmisión). Si no es especificado se asume 10", required=False, type=float, default=10)
parser.add_argument('-bmn','--betamn', help="Límite mínimo del parámetro beta (tasa de transmisión). Si no es especificado se asume 1", required=False, type=float, default=1)
parser.add_argument('-gm','--gamma', help="Tasa de recuperación. Si no es especificado se asume 1", required=False, type=float, default=1)
#Other parameters
parser.add_argument('-s','--salida', help="Nombre del archivo de salida. Si no es especificado se asume 'SIR_COVID-19_001.csv'", required=False, default="SIR_COVID-19_0001.csv")
parser.add_argument('-gf','--graficar', help="Graficar los datos de la simulación. Si no es especificado no se grafica", required=False, action='store_true')

parsed_args = vars(parser.parse_args())

# Arguments minus script name
args = sys.argv[1:]

#Datos de la simulacion
t0 = parsed_args['tiempo_inicial_sim']  #Tiempo inicial
tf = parsed_args['tiempo_final_sim']  #Tiempo final [dias]
hh = parsed_args['delta']  #Paso o delta de tiempo (dt) (Parametro suceptible al metodo de resolucion)
n = int((tf - t0) / hh) #Cantidad de datos esperados

#Condiciones iniciales
r0 = parsed_args['infeccion_inicial']      #Fraccion de Infeccion Inicial
if parsed_args['susceptible_inicial'] < 0:
    x0 = 1 - r0             #Fraccion Suceptible Inicial
else:
    x0 = parsed_args['susceptible_inicial']
y0 = r0                     #Fraccion de Infeccion Inicial
z0 = parsed_args['removidos_inicial']      #Fraccion de Removidos Inicial

#Parametros del modelo
betamx = parsed_args['betamx']           #Limite maximo del parametro beta
betamn = parsed_args['betamn']           #Límite minimo del parametro beta
beta = np.linspace(betamn,betamx,n+1)    #Creacion del arreglo beta[]
gamma = parsed_args['gamma']              #Valor del parametro gamma
#Other parameters
output = parsed_args['salida'] 

vt, vx, vy, vz = rk4(f, g, h, x0, y0, z0, t0, tf, beta, gamma, n, hh)

#no es necesario mostrar los datos en la salida estandar, puesto que se guardan en el archivo csv
#for t, x, y, z in list(zip(vt, vx, vy, vz))[::10]:
#    print("%5.1f %0.5f %0.5f %0.5f" % (t, x, y, z))

d = {'Tiempo': vt, 'Susceptibles': vx, 'Infectados': vy, 'Removidos': vz}
df = pd.DataFrame(data=d)
df.to_csv(output, index=False)

if parsed_args['graficar']:
    plt.plot(vt,vx,'-',linewidth=1,color='b', label = "Susceptibles")
    plt.plot(vt,vy,'-',linewidth=1,color='g', label = "Infectados")
    plt.plot(vt,vz,'-',linewidth=1,color='r', label = "Removidos")
    #plt.plot(vt,(beta-betamn)/(betamx-betamn),'-',linewidth=1,color='y', label = "Tasa")
    plt.grid()
    plt.xlim(t0,tf)
    plt.ylim(0,1)
    plt.xlabel('tiempo')
    plt.ylabel('Fracción Casos')
    plt.title('Modelo SIR')
    plt.legend()
    plt.show()
#Fin
