# app/__init__.py

from flask import Flask
from flask import request
from flask_cors import CORS
import mod_sir_covid_19_v1

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/sir01', methods=['GET', 'POST'])
    def sir01():
        r0 = request.args.get('r0', default = 0.0000045, type = float)
        x0 = request.args.get('x0', default = -1, type = float)
        z0 = request.args.get('z0', default = 0, type = float)
        t0 = request.args.get('t0', default = 0, type = int)
        tf = request.args.get('tf', default = 15, type = int)
        betamn = request.args.get('betamn', default = 1, type = float)
        betamx = request.args.get('betamx', default = 10, type = float)
        gamma = request.args.get('gamma', default = 1, type = float)
        hh = request.args.get('hh', default = 0.01, type = float)

        n = int((tf - t0) / hh)

        if x0 < 0:
            x0 = 1 - r0

        y0 = r0

        return mod_sir_covid_19_v1.rk4(mod_sir_covid_19_v1.f, mod_sir_covid_19_v1.g, mod_sir_covid_19_v1.h, x0, y0, z0, t0, tf, betamn, betamx, gamma, n, hh)

    @app.route('/sir02')
    def sir02():
        return 'Hello, SIR Analitico 2!'

    @app.route('/seir01')
    def seir01():
        return 'Hello, SEIR Analitico 1!'

    return app
