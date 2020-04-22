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
  constructor(private httpClient: HttpClient) {
  }

  ngOnInit() {
    this.sir001();
  }

  sir001() {
    /*this.httpClient.get<any>('http://127.0.0.1:5000/sir01')
      .toPromise()
      .then(res => <SIR01Data[]>res.data)
      .then(data => this.modSIR01Data = data);*/

    this.httpClient.get<any>('http://127.0.0.1:5000/sir01')
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
                    label: data['data']['index'][2],
                    data: data['data']['data'][2],
                    fill: false,
                    borderColor: '#565656'
                },
                {
                    label: data['data']['index'][3],
                    data: data['data']['data'][3],
                    fill: false,
                    borderColor: '#ff0000'
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
