# Adaptacion: 10/Abr/2020, por Egner Aceros, egner.aceros@gmail.com, TepuyRDGroup, http://tepuyrd.com/, twitter: @TepuyRDGroup
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
 
def rk4(f, g, h, i, w0, x0, y0, z0, t0, tf, alfa, beta, gamma, n, hh):
    vt = [0] * (n + 1)
    vw = [0] * (n + 1)
    vx = [0] * (n + 1)
    vy = [0] * (n + 1)
    vz = [0] * (n + 1)
    #hh = 0.01
    vt[0] = t = t0
    vw[0] = w = w0
    vx[0] = x = x0
    vy[0] = y = y0
    vz[0] = z = z0
    ii = 0
    while t < tf:
    #for i in range(1, n + 1):
        k1 = hh * f(w, x, y, z, alfa, beta[ii], gamma)
        l1 = hh * g(w, x, y, z, alfa, beta[ii], gamma)
        m1 = hh * h(w, x, y, z, alfa, beta[ii], gamma)
        n1 = hh * i(w, x, y, z, alfa, beta[ii], gamma)
        k2 = hh * f(w + k1/2, x + l1/2, y + m1/2, z + n1/2, alfa, beta[ii], gamma)
        l2 = hh * g(w + k1/2, x + l1/2, y + m1/2, z + n1/2, alfa, beta[ii], gamma)
        m2 = hh * h(w + k1/2, x + l1/2, y + m1/2, z + n1/2, alfa, beta[ii], gamma)
        n2 = hh * i(w + k1/2, x + l1/2, y + m1/2, z + n1/2, alfa, beta[ii], gamma)
        k3 = hh * f(w + k2/2, x + l2/2, y + m2/2, z + n2/2, alfa, beta[ii], gamma)
        l3 = hh * g(w + k2/2, x + l2/2, y + m2/2, z + n2/2, alfa, beta[ii], gamma)
        m3 = hh * h(w + k2/2, x + l2/2, y + m2/2, z + n2/2, alfa, beta[ii], gamma)
        n3 = hh * i(w + k2/2, x + l2/2, y + m2/2, z + n2/2, alfa, beta[ii], gamma)
        k4 = hh * f(w + k3, x + l3, y + m3, z + n3, alfa, beta[ii], gamma)
        l4 = hh * g(w + k3, x + l3, y + m3, z + n3, alfa, beta[ii], gamma)
        m4 = hh * h(w + k3, x + l3, y + m3, z + n3, alfa, beta[ii], gamma)
        n4 = hh * h(w + k3, x + l3, y + m3, z + n3, alfa, beta[ii], gamma)
        vt[ii] = t = t0 + ii * hh
        vw[ii] = w = w + (k1 + 2*k2 + 2*k3 + k4) / 6
        vx[ii] = x = x + (l1 + 2*l2 + 2*l3 + l4) / 6
        vy[ii] = y = y + (m1 + 2*m2 + 2*m3 + m4) / 6
        vz[ii] = z = z + (n1 + 2*n2 + 2*n3 + n4) / 6

        ii = ii + 1
    return vt, vw, vx, vy, vz
 
def f(w, x, y, z, alfa, beta, gamma):
    return (-beta*y*w)

def g(w, x, y, z, alfa, beta, gamma):
    return (beta*y*w - alfa*x)

def h(w, x, y, z, alfa, beta, gamma):
    return (alfa*x - gamma*y)

def i(w, x, y, z, alfa, beta, gamma):
    return (gamma*y)



#Inicio

parser = argparse.ArgumentParser(description='Modelo analítico COVID19 basado en SEIR (Susceptibles, Expuestos, Infectados, Removidos)')

#Datos de la simulacion
parser.add_argument('-t0','--tiempo-inicial-sim', help="Tiempo inicial de simulación en días. Si no es especificado se asume 0", required=False, type=int, default=0)
parser.add_argument('-tf','--tiempo-final-sim', help="Tiempo final de simulación en días. Si no es especificado se asume 15 días", required=False, type=int, default=15)
parser.add_argument('-hh','--delta', help="Paso o delta de tiempo (dt). Este parametro es suceptible al método de resolucion. Si no es especificado se asume 0.01 días", required=False, type=float, default=0.01)
#Condiciones iniciales
#parser.add_argument('-r0','---infeccion-inicial', help="Fraccion de Infeccion Inicial. Si no es especificado se asume 0.0000045", required=False, type=float, default=0.0000045)
parser.add_argument('-x0','--expuestos-inicial', help="Fraccion de Expuestos Inicial. Si no es especificado se asume 0.1", required=False, type=float, default=0.1)
parser.add_argument('-w0','--susceptible-inicial', help="Fraccion Suceptible Inicial. Si no es especificado se asume 1 - x0", required=False, type=float, default=-1)
parser.add_argument('-y0','--infeccion-inicial', help="Fracción de Infeccion Inicial. Si no es especificado se asume 0", required=False, type=float, default=0)
parser.add_argument('-z0','--removidos-inicial', help="Fraccion de Removidos Inicial. Si no es especificado se asume 0", required=False, type=float, default=0)
#Parametros del modelo
parser.add_argument('-bmx','--betamx', help="Límite máximo del parámetro beta (tasa de transmisión). Si no es especificado se asume 10", required=False, type=float, default=10)
parser.add_argument('-bmn','--betamn', help="Límite mínimo del parámetro beta (tasa de transmisión). Si no es especificado se asume 9", required=False, type=float, default=9)
parser.add_argument('-gm','--gamma', help="Tasa de recuperación. Si no es especificado se asume 1", required=False, type=float, default=1)
parser.add_argument('-af','--alfa', help="Tasa de exposición. Si no es especificado se asume 2", required=False, type=float, default=2)

#Other parameters
parser.add_argument('-s','--salida', help="Nombre del archivo de salida. Si no es especificado se asume 'SIR_COVID-19_001.csv'", required=False, default="SEIR_COVID-19_0001.csv")
parser.add_argument('-gf','--graficar', help="Graficar los datos de la simulación. Si no es especificado no se grafica", required=False, action='store_true')

parsed_args = vars(parser.parse_args())

# Arguments minus script name
args = sys.argv[1:]

t0 = parsed_args['tiempo_inicial_sim']
tf = parsed_args['tiempo_final_sim']
hh = parsed_args['delta']
n = int((tf - t0) / hh)

#r0 = 0.0000045 #r0 no es usado en este algoritmo
x0 = parsed_args['expuestos_inicial']
if parsed_args['susceptible_inicial'] < 0:
    w0 = 1 - x0             
else:
    w0 = parsed_args['susceptible_inicial']

#x0 = 10*r0
y0 = parsed_args['infeccion_inicial']
z0 = parsed_args['removidos_inicial']
#n = 100
#hh = 0.1
betamx = parsed_args['betamx']
betamn = parsed_args['betamn']

beta = np.linspace(betamn,betamx,n+1)
gamma = parsed_args['gamma'] 
alfa = parsed_args['alfa'] 

#Other parameters
output = parsed_args['salida'] 

vt, vw, vx, vy, vz = rk4(f, g, h, i, w0, x0, y0, z0, t0, tf, alfa, beta, gamma, n, hh)
#for t, w, x, y, z in list(zip(vt, vw, vx, vy, vz))[::10]:
#    print("%5.1f %0.5f %0.5f %0.5f %0.5f" % (t, w, x, y, z))

d = {'Tiempo': vt, 'Susceptibles': vw, 'Expuestos': vx, 'Infectados': vy, 'Removidos': vz}
df = pd.DataFrame(data=d)
df.to_csv(output, index=False)

if parsed_args['graficar']:
    plt.plot(vt,vw,'-',linewidth=1,color='b', label = "Susceptibles")
    plt.plot(vt,vx,'-',linewidth=1,color='k', label = "Expuestos")
    plt.plot(vt,vy,'--',linewidth=1,color='r', label = "Infectados")
    plt.plot(vt,vz,'-',linewidth=1,color='g', label = "Removidos")
    #plt.plot(vt,(beta-betamn)/(betamx-betamn),'-',linewidth=1,color='y', label = "Tasa")
    plt.grid()
    plt.xlim(t0,tf)
    plt.ylim(0,1)
    plt.xlabel('tiempo')
    plt.ylabel('Fracción Casos')
    plt.title('Modelo SEIR')
    plt.legend()
    plt.show()
