# Adaptacion: 29/Mar/2020, por Egner Aceros, egner.aceros@gmail.com, TepuyRDGroup, http://tepuyrd.com/, twitter: @TepuyRDGroup
# Equipo 4: Modelo para predecir la propagación del COVID19

# Referencia 1: Castro P., De los Reyes J. , Gonzalez S., Merino P., Ponce J.,
# "Modelización y Simulación de la propagación del virus sars-cov-2 en Ecuador"
# Centro de Modelización Matemática en Áreas Clave para el Desarrollo, MODEMAT
# Escuela Politécnica Nacional de Ecuador. modemat@epn.edu.ec, 26 de marzo de 2020

# Referencia 2: https://rosettacode.org/wiki/Runge-Kutta_method

import numpy as np
import pandas as pd

def f(x, y, z, beta, gamma):
    return (-beta*y*x)

def g(x, y, z, beta, gamma):
    return (beta*x - gamma)*y

def h(x, y, z, beta, gamma):
    return (gamma*y)
 
def rk4(f, g, h, x0, y0, z0, t0, tf, betamn, betamx, gamma, n, hh):
    beta = np.linspace(betamn,betamx,n+1)    #Creacion del arreglo beta[]
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


    d = {'tiempo': vt, 'susceptibles': vx, 'infectados': vy, 'removidos': vz}
    #df = pd.DataFrame(data=d)
    df = pd.DataFrame([vt, vx, vy, vz], index =['tiempo', 'susceptibles', 'infectados', 'removidos'])
    return '{ "data": ' + df.to_json(orient='split') + '}'
