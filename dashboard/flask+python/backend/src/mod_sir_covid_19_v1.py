# Adaptacion: 29/Mar/2020, por Egner Aceros, egner.aceros@gmail.com, TepuyRDGroup, http://tepuyrd.com/, twitter: @TepuyRDGroup
# Equipo 4: Modelo para predecir la propagación del COVID19

# Referencia 1: Castro P., De los Reyes J. , Gonzalez S., Merino P., Ponce J.,
# "Modelización y Simulación de la propagación del virus sars-cov-2 en Ecuador"
# Centro de Modelización Matemática en Áreas Clave para el Desarrollo, MODEMAT
# Escuela Politécnica Nacional de Ecuador. modemat@epn.edu.ec, 26 de marzo de 2020

# Referencia 2: https://rosettacode.org/wiki/Runge-Kutta_method

import numpy as np
import pandas as pd
import sys
import ssl
from urllib.request import urlopen
import json
import urllib.request
import os
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from datetime import timedelta, datetime


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

    df = pd.DataFrame([vt, vx, vy, vz], index =['tiempo', 'susceptibles', 'infectados', 'removidos'])
    return '{ "data": ' + df.to_json(orient='split') + '}'

def remove_all_series_province(url_dictionary):
    for url_title in url_dictionary.keys():
        filename, extension = os.path.splitext(url_title)
        inputfile = os.path.join('/tmp', url_title)
        outputfile = os.path.join('/tmp', "{}-country{}".format(filename, extension))
        remove_province(inputfile, outputfile)

def remove_province(input_file, output_file):
    input = open(input_file, "r")
    output = open(output_file, "w")
    output.write(input.readline())
    for line in input:
        if line.lstrip().startswith(","):
            output.write(line)
    input.close()
    output.close()

def download_dataset():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://raw.githubusercontent.com/Lewuathe/COVID19-SIR/master/data_url.json'
    json_url = urlopen(url)
    response = json.load(json_url)

    return response

def download_data(url_dictionary):
    #Lets download the files
    for url_title in url_dictionary.keys():
        fullfilename = os.path.join('/tmp', url_title)
        urllib.request.urlretrieve(url_dictionary[url_title], fullfilename)


def load_json(json_file_str):
    # Loads  JSON into a dictionary or quits the program if it cannot.
    try:
        with open(json_file_str, "r") as json_file:
            json_variable = json.load(json_file)
            return json_variable
    except Exception:
        sys.exit("Cannot open JSON file: " + json_file_str)


def loss(point, data, recovered, s_0, i_0, r_0):
    size = len(data)
    beta, gamma = point
    def SIR(t, y):
        S = y[0]
        I = y[1]
        R = y[2]
        return [-beta*S*I, beta*S*I-gamma*I, gamma*I]
    solution = solve_ivp(SIR, [0, size], [s_0,i_0,r_0], t_eval=np.arange(0, size, 1), vectorized=True)
    l1 = np.sqrt(np.mean((solution.y[1] - data)**2))
    l2 = np.sqrt(np.mean((solution.y[2] - recovered)**2))
    alpha = 0.1
    return alpha * l1 + (1 - alpha) * l2

class Learner(object):
    def __init__(self, country, loss, start_date, predict_range, s_0, i_0, r_0):
        self.country = country
        self.loss = loss
        self.start_date = start_date
        self.predict_range = predict_range
        self.s_0 = s_0
        self.i_0 = i_0
        self.r_0 = r_0

    def load_confirmed(self, country):
        df = pd.read_csv('/tmp/time_series_19-covid-Confirmed-country.csv')
        country_df = df[df['Country/Region'] == country]
        return country_df.iloc[0].loc[self.start_date:]


    def load_recovered(self, country):
        df = pd.read_csv('/tmp/time_series_19-covid-Recovered-country.csv')
        country_df = df[df['Country/Region'] == country]
        return country_df.iloc[0].loc[self.start_date:]


    def load_dead(self, country):
        df = pd.read_csv('/tmp/time_series_19-covid-Deaths-country.csv')
        country_df = df[df['Country/Region'] == country]
        return country_df.iloc[0].loc[self.start_date:]
    

    def extend_index(self, index, new_size):
        values = index.values
        current = datetime.strptime(index[-1], '%m/%d/%y')
        while len(values) < new_size:
            current = current + timedelta(days=1)
            values = np.append(values, datetime.strftime(current, '%m/%d/%y'))
        return values
    
    
    def predict(self, beta, gamma, data, recovered, death, country, s_0, i_0, r_0):
        new_index = self.extend_index(data.index, self.predict_range)
        size = len(new_index)
        def SIR(t, y):
            S = y[0]
            I = y[1]
            R = y[2]
            return [-beta*S*I, beta*S*I-gamma*I, gamma*I]
        extended_actual = np.concatenate((data.values, [None] * (size - len(data.values))))
        extended_recovered = np.concatenate((recovered.values, [None] * (size - len(recovered.values))))
        extended_death = np.concatenate((death.values, [None] * (size - len(death.values))))
        return new_index, extended_actual, extended_recovered, extended_death, solve_ivp(SIR, [0, size], [s_0,i_0,r_0], t_eval=np.arange(0, size, 1))

    # Find $\beta$ and $\gamma$
    def train(self):
        recovered = self.load_recovered(self.country)
        death = self.load_dead(self.country)
        data = (self.load_confirmed(self.country) - recovered - death)
        optimal = minimize(loss, [0.001, 0.001], args=(data, recovered, self.s_0, self.i_0, self.r_0), method='L-BFGS-B', bounds=[(0.00000001, 0.4), (0.00000001, 0.4)])
        beta, gamma = optimal.x
        new_index, extended_actual, extended_recovered, extended_death, prediction = self.predict(beta, gamma, data, recovered, death, self.country, self.s_0, self.i_0, self.r_0)
        df = pd.DataFrame([extended_actual, extended_recovered, extended_death, prediction.y[0],  prediction.y[1], prediction.y[2]], index =['Infected data', 'Recovered data', 'Death data', 'Susceptible', 'Infected', 'Recovered'])
       
        return '{ "data": ' + df.to_json(orient='split') + '}'


