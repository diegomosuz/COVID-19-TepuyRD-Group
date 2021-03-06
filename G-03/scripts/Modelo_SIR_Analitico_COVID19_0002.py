# Adaptacion: 09/Abr/2020, por Egner Aceros, egner.aceros@gmail.com, TepuyRDGroup, http://tepuyrd.com/, twitter: @TepuyRDGroup
# Equipo 4: Modelo para predecir la propagación del COVID19

# Referencia: https://colab.research.google.com/drive/1aDgRmUWS21rtbo2Y7IMO0tC8--jtsgF-#scrollTo=0q8dJ5aJI13m

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
import sys
import json
import ssl
import urllib.request
import argparse

import os
import wget

#inicio
parser = argparse.ArgumentParser(description='Modelo analítico COVID19 basado en SIR (Susceptibles, Infectados, Removidos)')

#Datos de la simulacion
parser.add_argument('-lp','--lista-paises', help="Lista de paises ex. Ecuador,Venezuela,Colombia.", required=True)
parser.add_argument('-fi','--fecha-inicio', help="Fecha de inicio de la simulación en formato mm/dd/yyyy. Si no es específicado se asume 1/22/2020", required=False, default="1/22/20")
parser.add_argument('-rp','--rango-predicho', help="Rango predicho en días. Si no es especificado se asume 150 días", required=False, type=int, default=150)
#Condiciones iniciales
parser.add_argument('-i0','---infeccion-inicial', help="Fraccion de Infeccion Inicial. Si no es especificado se asume 2", required=False, type=int, default=2)
parser.add_argument('-s0','--susceptible-inicial', help="Fraccion Suceptible Inicial. Si no es especificado se asume 4000000", required=False, type=int, default=4000000)
parser.add_argument('-r0','--removidos-inicial', help="Fraccion Removidos Inicial. Si no es especificado se asume 10", required=False, type=int, default=10)
#Other parameters
parser.add_argument('-s','--salida', help="Prefijo del nombre del archivo de salida. Si no es especificado se asume 'SIR_COVID-19_001'", required=False, default="SIR_COVID-19_0002")
#parser.add_argument('-gf','--graficar', help="Graficar los datos de la simulación. Si no es especificado no se grafica", required=False, action='store_true')
parser.add_argument('-nd','--no-descargar', help="Omitir la descarga de datos desde el repositorio.", required=False, action='store_false')

parsed_args = vars(parser.parse_args())

# Arguments minus script name
args = sys.argv[1:]

countries=parsed_args['lista_paises'].split(",")
download=parsed_args['no_descargar']
output=parsed_args['salida']
#graficar=parsed_args['graficar']
startdate=parsed_args['fecha_inicio']
predict_range=parsed_args['rango_predicho']
s_0=parsed_args['susceptible_inicial']
i_0 = parsed_args['infeccion_inicial']
r_0 = parsed_args['removidos_inicial']

#! mkdir data 
#%cd data
#! wget https://raw.githubusercontent.com/Lewuathe/COVID19-SIR/master/data_url.json

# Directory
print("\nSe descargarán los archivos con los datos\n")
directory = "data"
# Parent Directory path 
parent_dir = "."
# Path 
path = os.path.join(parent_dir, directory) 
#os.mkdir(path) 
#print("Directory '%s' created" %directory) 
os.chdir(directory)
ssl._create_default_https_context = ssl._create_unverified_context
url = 'https://raw.githubusercontent.com/Lewuathe/COVID19-SIR/master/data_url.json'
filename = wget.download(url)
print("\nLos datos fueron descargados\n")

class Learner(object):
    def __init__(self, country, loss, start_date, predict_range,s_0, i_0, r_0):
        self.country = country
        self.loss = loss
        self.start_date = start_date
        self.predict_range = predict_range
        self.s_0 = s_0
        self.i_0 = i_0
        self.r_0 = r_0
        print("\nInicializo la variable Learner\n")



    def load_confirmed(self, country):
        df = pd.read_csv('time_series_19-covid-Confirmed-country.csv')
        country_df = df[df['Country/Region'] == country]
        return country_df.iloc[0].loc[self.start_date:]


    def load_recovered(self, country):
        df = pd.read_csv('time_series_19-covid-Recovered-country.csv')
        country_df = df[df['Country/Region'] == country]
        return country_df.iloc[0].loc[self.start_date:]


    def load_dead(self, country):
        df = pd.read_csv('time_series_19-covid-Deaths-country.csv')
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
        print("cargo recuperados")
        death = self.load_dead(self.country)
        print("cargo fallecidos")
        data = (self.load_confirmed(self.country) - recovered - death)
        print("cargo datos = confirmados - recuperados - fallecidos")
        print("aplicando el metodo de optimizacion por L-BFGS-B, tenga paciencia puede durar horas")
        optimal = minimize(loss, [0.001, 0.001], args=(data, recovered, self.s_0, self.i_0, self.r_0), method='L-BFGS-B', bounds=[(0.00000001, 0.4), (0.00000001, 0.4)])
        print("halló puntos óptimos de beta y gamma, por el método L-BFGS-B")
        beta, gamma = optimal.x
        new_index, extended_actual, extended_recovered, extended_death, prediction = self.predict(beta, gamma, data, recovered, death, self.country, self.s_0, self.i_0, self.r_0)
        print("calculo valores predichos")
        df = pd.DataFrame({'Infected data': extended_actual, 'Recovered data': extended_recovered, 'Death data': extended_death, 'Susceptible': prediction.y[0], 'Infected': prediction.y[1], 'Recovered': prediction.y[2]}, index=new_index)
        print("halló el dataframe")
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_title(self.country)
        df.plot(ax=ax)
        print(f"country={self.country}, beta={beta:.8f}, gamma={gamma:.8f}, r_0:{(beta/gamma):.8f}")
        fig.savefig(f"{self.country}.png")

        #save the data to a file
        fileout="{}-{}.csv".format(output, self.country) 
        df.to_csv(fileout, index=True)

def remove_province(input_file, output_file):
    input = open(input_file, "r")
    output = open(output_file, "w")
    output.write(input.readline())
    for line in input:
        if line.lstrip().startswith(","):
            output.write(line)
    input.close()
    output.close()
  

def download_data(url_dictionary):
    #Lets download the files
    for url_title in url_dictionary.keys():
        urllib.request.urlretrieve(url_dictionary[url_title], url_title)


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

def main():

    if download:
        data_d = load_json("data_url.json")
        download_data(data_d)

    remove_province('time_series_19-covid-Confirmed.csv', 'time_series_19-covid-Confirmed-country.csv')
    remove_province('time_series_19-covid-Recovered.csv', 'time_series_19-covid-Recovered-country.csv')
    remove_province('time_series_19-covid-Deaths.csv', 'time_series_19-covid-Deaths-country.csv')

    for country in countries:
    	print("\nAnalizando el país: ",country)
    	learner = Learner(country, loss, startdate, predict_range, s_0, i_0, r_0)
    	learner.train()   

if __name__ == '__main__':
    main()
