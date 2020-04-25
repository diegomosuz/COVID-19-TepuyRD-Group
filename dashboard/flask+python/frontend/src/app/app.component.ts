import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


export class SIR01Data {
  modData: any;
  modDataInf: any;
  simdays: number; // numero de días
  tstart: number;  // tiempo inicial
  r0: number;      // cantidad inicial de contagiados max 1
  x0: number;      // susceptibles max 1
  z0: number;      // removidos max 1
  betamn: number;  // velocidad de contagio máximo
  betamx: number;  // velocidad de contagio mínimo
  gamma: number;   // velocidad de recuperación
  hh: number;      // paso del modelo

  constructor(){
    this.tstart=0;
    this.simdays=15;
    this.r0=0.0000045;
    this.x0=-1;
    this.z0=0;
    this.betamn=2;
    this.betamx=5;
    this.gamma=1;
    this.hh=0.01;
  }
}

export class SEIR01Data extends SIR01Data {
    w0: number;      // suceptibles in the SEIR model
    alfa: number;    // tasa de exposicion

  constructor(){
    super();
    this.tstart=0;
    this.simdays=15;
    this.r0=0;
    this.x0=0.1;
    this.z0=0;
    this.w0=-1;
    this.betamn=9;
    this.betamx=10;
    this.gamma=1;
    this.alfa=2;
    this.hh=0.01;
  }
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'frontend';
  sir01Data: SIR01Data;
  seir01Data: SEIR01Data;
  blockedPnlSIR01: boolean = false;
  blockedPnlSEIR: boolean = false;
  

  constructor(private httpClient: HttpClient) {
    this.sir01Data = new SIR01Data;
    this.seir01Data = new SEIR01Data;    
  }

  ngOnInit() {
    this.sir001();
    this.seir001();
  }

  sir001() {
    let tf=this.sir01Data.tstart+this.sir01Data.simdays;
    this.blockedPnlSIR01 = true;
    this.httpClient.get<any>(`http://127.0.0.1:5000/sir01?t0=${this.sir01Data.tstart}&tf=${tf}&r0=${this.sir01Data.r0}&x0=${this.sir01Data.x0}&z0=${this.sir01Data.z0}&betamn=${this.sir01Data.betamn}&betamx=${this.sir01Data.betamx}&gamma=${this.sir01Data.gamma}&hh=${this.sir01Data.hh}`)
      .subscribe((data: JSON) => {
         this.sir01Data.modData = {
            labels: data['data']['data'][0],
            datasets: [
                {
                    label: data['data']['index'][1],
                    data: data['data']['data'][1],
                    fill: false,
                    borderColor: '#4bc0c0'
                },
                {
                    label: data['data']['index'][3],
                    data: data['data']['data'][3],
                    fill: false,
                    borderColor: '#ff0000'
                }
            ]
        };

        this.sir01Data.modDataInf = {
            labels: data['data']['data'][0],
            datasets: [
                {
                    label: data['data']['index'][2],
                    data: data['data']['data'][2],
                    fill: false,
                    borderColor: '#565656'
                }
            ]
        }
        this.blockedPnlSIR01 = false;
      });
  }

  sir002() {
  }

  seir001() {
    let tf=this.seir01Data.tstart+this.seir01Data.simdays;
    this.blockedPnlSEIR = true;
    this.httpClient.get<any>(`http://127.0.0.1:5000/seir01?t0=${this.seir01Data.tstart}&tf=${tf}&r0=${this.seir01Data.r0}&x0=${this.seir01Data.x0}&w0=${this.seir01Data.w0}&z0=${this.seir01Data.z0}&betamn=${this.seir01Data.betamn}&betamx=${this.seir01Data.betamx}&gamma=${this.seir01Data.gamma}&alfa=${this.seir01Data.alfa}&hh=${this.seir01Data.hh}`)
      .subscribe((data: JSON) => {
         this.seir01Data.modData = {
            labels: data['data']['data'][0],
            datasets: [
                {
                    label: data['data']['index'][1],
                    data: data['data']['data'][1],
                    fill: false,
                    borderColor: '#4bc0c0'
                },
                {
                    label: data['data']['index'][4],
                    data: data['data']['data'][4],
                    fill: false,
                    borderColor: '#ff0000'
                }
            ]
        };

        this.seir01Data.modDataInf = {
            labels: data['data']['data'][0],
            datasets: [
                {
                    label: data['data']['index'][2],
                    data: data['data']['data'][2],
                    fill: false,
                    borderColor: '#565656'
                },
                {
                    label: data['data']['index'][3],
                    data: data['data']['data'][3],
                    fill: false,
                    borderColor: '#00ff00'
                }
            ]
        }
        this.blockedPnlSEIR = false;
      });
  }
}
