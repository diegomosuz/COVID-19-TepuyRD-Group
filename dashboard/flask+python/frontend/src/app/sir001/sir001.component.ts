import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { SelectItem } from 'primeng/api';
import { DatePipe } from '@angular/common';
import { environment } from '../../environments/environment';

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

@Component({
  selector: 'app-sir001',
  templateUrl: './sir001.component.html',
  styleUrls: ['./sir001.component.css']
})
export class Sir001Component implements OnInit {
  sir01Data: SIR01Data;
  blockedPnlSIR01: boolean = false;
  baseApiUrl = environment.baseApiUrl;
  constructor(private httpClient: HttpClient, private datePipe: DatePipe) {
    this.sir01Data = new SIR01Data;
  }

  ngOnInit(): void {
    this.updateModel();
  }

  updateModel() {
    let tf=this.sir01Data.tstart+this.sir01Data.simdays;
    this.blockedPnlSIR01 = true;
    this.httpClient.get<any>(`${this.baseApiUrl}/sir01?t0=${this.sir01Data.tstart}&tf=${tf}&r0=${this.sir01Data.r0}&x0=${this.sir01Data.x0}&z0=${this.sir01Data.z0}&betamn=${this.sir01Data.betamn}&betamx=${this.sir01Data.betamx}&gamma=${this.sir01Data.gamma}&hh=${this.sir01Data.hh}`)
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
      },
      error => this.blockedPnlSIR01 = false);
  }
}
