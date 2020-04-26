# app/__init__.py

from flask import Flask
from flask import request
from flask_cors import CORS
import mod_sir_covid_19_v1 as sirv1
import mod_seir_covid_19_v1 as seir

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/sir01', methods=['GET', 'POST'])
    def sir01():
        try:
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

            return sirv1.rk4(sirv1.f, sirv1.g, sirv1.h, x0, y0, z0, t0, tf, betamn, betamx, gamma, n, hh)
        except (RuntimeError, TypeError, NameError, Exception):
            return '{ "data": {"columns":[],"index":["fecha","Invalid parameters","Invalid parameters","Invalid parameters","Invalid parameters","Invalid parameters","Invalid parameters"],"data":[[],[],[],[],[],[],[]]} }';

    @app.route('/sir02')
    def sir02():
        try:
            country = request.args.get('country', default = "Colombia", type = str)
            fi = request.args.get('fi', default="1/22/20", type = str)
            rp = request.args.get('rp', default = 30, type = int)
            i0 = request.args.get('i0', default = 2, type = int)
            s0 = request.args.get('s0', default = 200000, type = int)
            r0 = request.args.get('r0', default = 10, type = float)

            print(country, fi, rp, i0, s0, r0)

            data_d = sirv1.download_dataset()
            sirv1.download_data(data_d)
            sirv1.remove_all_series_province(data_d)

            learner = sirv1.Learner(country, sirv1.loss, fi, rp, s0, i0, r0)
            return learner.train()
        except (RuntimeError, TypeError, NameError, Exception):
            return '{ "data": {"columns":[],"index":["fecha","Invalid parameters","Invalid parameters","Invalid parameters","Invalid parameters","Invalid parameters","Invalid parameters"],"data":[[],[],[],[],[],[],[]]} }';

    @app.route('/seir01')
    def seir01():
        try:
            r0 = request.args.get('r0', default = 0, type = float)
            x0 = request.args.get('x0', default = 0.1, type = float)
            w0 = request.args.get('w0', default = -1, type = float)
            z0 = request.args.get('z0', default = 0, type = float)
            t0 = request.args.get('t0', default = 0, type = int)
            tf = request.args.get('tf', default = 15, type = int)
            betamn = request.args.get('betamn', default = 9, type = float)
            betamx = request.args.get('betamx', default = 10, type = float)
            gamma = request.args.get('gamma', default = 1, type = float)
            alfa = request.args.get('alfa', default = 2, type = float)
            hh = request.args.get('hh', default = 0.01, type = float)

            n = int((tf - t0) / hh)

            if w0 < 0:
                w0 = 1 - r0

            y0 = r0

            return seir.rk4(seir.f, seir.g, seir.h, seir.i, w0, x0, y0, z0, t0, tf, alfa, betamn, betamx, gamma, n, hh)
        except (RuntimeError, TypeError, NameError, Exception):
            return '{ "data": {"columns":[],"index":["fecha","Invalid parameters","Invalid parameters","Invalid parameters","Invalid parameters","Invalid parameters","Invalid parameters"],"data":[[],[],[],[],[],[],[]]} }';


    return app
