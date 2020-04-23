import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


/*export interface SIR01Data {
  tiempo;
  susceptibles;
  infectados;
  removidos;
}*/

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'frontend';
  modSIR01Data: any;
  modSIR01DataInf: any;
  simdays: number; // numero de días
  tstart: number;  // tiempo inicial
  r0: number;      // cantidad inicial de contagiados max 1
  x0: number;      // susceptibles max 1
  z0: number;      // removidos max 1
  betamn: number;  // velocidad de contagio máximo
  betamx: number;  // velocidad de contagio mínimo
  gamma: number;   // velocidad de recuperación
  hh: number;      // paso del modelo

  constructor(private httpClient: HttpClient) {
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

  ngOnInit() {
    this.sir001();
  }

  sir001() {
    /*this.httpClient.get<any>('http://127.0.0.1:5000/sir01')
      .toPromise()
      .then(res => <SIR01Data[]>res.data)
      .then(data => this.modSIR01Data = data);*/

    let tf=this.tstart+this.simdays;
    this.httpClient.get<any>(`http://127.0.0.1:5000/sir01?t0=${this.tstart}&tf=${tf}&r0=${this.r0}&x0=${this.x0}&z0=${this.z0}&betamn=${this.betamn}&betamx=${this.betamx}&gamma=${this.gamma}&hh=${this.hh}`)
      .subscribe((data: JSON) => {
         this.modSIR01Data = {
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

        this.modSIR01DataInf = {
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
      });
  }

  sir002() {
    /*this.httpClient.get('http://localhost:5000/sir02').subscribe(data => {
      this.modSIR02Data = data as JSON;
      console.log(this.modSIR02Data);
    })*/

        /*this.httpClient.get<any>('http://127.0.0.1:5000/sir01')
          .toPromise()
          .then(res => <SIR01Data[]>res.data)
          .then(data => this.modSIR01Data = data);*/

   /* this.httpClient.get<any>('http://127.0.0.1:5000/sir01')
      .subscribe((data : any[]) => {
        /*this.data.labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
        this.data.datasets[0].data = [65, 59, 80, 81, 56, 55, 40]
        this.data.datasets[0].label = 'Infectados';
	this.data.datasets[0].fill = false;
        this.data.datasets[0].borderColor= '#4bc0c0';*/

        /*this.data = {
            labels: data.data[0],
            datasets: [
                {
                    label: data.columns[1],
                    data: data.data[1],
                    fill: false,
                    borderColor: '#4bc0c0'
                },
                {
                    label: data.columns[2],
                    data: data.data[2],
                    fill: false,
                    borderColor: '#565656'
                }
            ]
        }
      });*/

      /*this.data = {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            datasets: [
                {
                    label: 'First Dataset',
                    data: [65, 59, 80, 81, 56, 55, 40],
                    fill: false,
                    borderColor: '#4bc0c0'
                },
                {
                    label: 'Second Dataset',
                    data: [28, 48, 40, 19, 86, 27, 90],
                    fill: false,
                    borderColor: '#565656'
                }
            ]
        }*/
  }
}
