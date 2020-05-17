import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { SelectItem } from 'primeng/api';
import { DatePipe } from '@angular/common';
import { environment } from '../../environments/environment';

export class SIR02Data {
  modData: any;
  modDataInf: any;
  paises: SelectItem[];
  paisElegido: string;
  date: Date;
  minDate: Date;
  fi: string; // fecha de inicio
  rp: number; // numero de dias a predecir
  i0: number; // Fracción Infección Inicial
  s0: number; // Fracción Susceptible Inicial
  r0: number; // Fracción Removidos Inicial

  constructor(){
    this.date = new Date("1/22/2020");
    this.minDate = new Date("1/22/2020");
    this.fi = "1/22/20";
    this.rp = 30;
    this.i0 = 2;
    this.s0 = 200000;
    this.r0 = 10;

    this.paises = [
      {label: "Afghanistan", value: "Afghanistan"}, {label: "Albania", value: "Albania"},
      {label: "Algeria", value: "Algeria"}, {label: "Andorra", value: "Andorra"},
      {label: "Angola", value: "Angola"}, {label: "Antigua and Barbuda", value: "Antigua and Barbuda"},
      {label: "Argentina", value: "Argentina"}, {label: "Armenia", value: "Armenia"},
      {label: "Austria", value: "Austria"}, {label: "Azerbaijan", value: "Azerbaijan"},
      {label: "Bahamas", value: "Bahamas"}, {label: "Bahrain", value: "Bahrain"},
      {label: "Bangladesh", value: "Bangladesh"}, {label: "Barbados", value: "Barbados"},
      {label: "Belarus", value: "Belarus"}, {label: "Belgium", value: "Belgium"},
      {label: "Benin", value: "Benin"}, {label: "Bhutan", value: "Bhutan"},
      {label: "Bolivia", value: "Bolivia"}, {label: "Bosnia and Herzegovina", value: "Bosnia and Herzegovina"},
      {label: "Brazil", value: "Brazil"}, {label: "Brunei", value: "Brunei"},
      {label: "Bulgaria", value: "Bulgaria"}, {label: "Burkina Faso", value: "Burkina Faso"},
      {label: "Cabo Verde", value: "Cabo Verde"}, {label: "Cambodia", value: "Cambodia"},
      {label: "Cameroon", value: "Cameroon"}, {label: "Central African Republic", value: "Central African Republic"},
      {label: "Chad", value: "Chad"}, {label: "Chile", value: "Chile"},
      {label: "Colombia", value: "Colombia"}, {label: "Congo (Brazzaville)", value: "Congo (Brazzaville)"},
      {label: "Congo (Kinshasa)", value: "Congo (Kinshasa)"},
      {label: "Costa Rica", value: "Costa Rica"}, {label: "Cote d'Ivoire", value: "Cote d'Ivoire"},
      {label: "Croatia", value: "Croatia"}, {label: "Diamond Princess", value: "Diamond Princess"},
      {label: "Cuba", value: "Cuba"}, {label: "Cyprus", value: "Cyprus"},
      {label: "Czechia", value: "Czechia"}, {label: "Denmark", value: "Denmark"},
      {label: "Djibouti", value: "Djibouti"}, {label: "Dominican Republic", value: "Dominican Republic"},
      {label: "Ecuador", value: "Ecuador"}, {label: "Egypt", value: "Egypt"},
      {label: "El Salvador", value: "El Salvador"}, {label: "Equatorial Guinea", value: "Equatorial Guinea"},
      {label: "Eritrea", value: "Eritrea"}, {label: "Estonia", value: "Estonia"},
      {label: "Eswatini", value: "Eswatini"}, {label: "Ethiopia", value: "Ethiopia"},
      {label: "Fiji", value: "Fiji"}, {label: "Finland", value: "Finland"},
      {label: "France", value: "France"}, {label: "Gabon", value: "Gabon"},
      {label: "Gambia", value: "Gambia"}, {label: "Georgia", value: "Georgia"},
      {label: "Germany", value: "Germany"}, {label: "Ghana", value: "Ghana"},
      {label: "Greece", value: "Greece"}, {label: "Guatemala", value: "Guatemala"},
      {label: "Guinea", value: "Guinea"}, {label: "Guyana", value: "Guyana"},
      {label: "Haiti", value: "Haiti"}, {label: "Holy See", value: "Holy See"},
      {label: "Honduras", value: "Honduras"}, {label: "Hungary", value: "Hungary"},
      {label: "Iceland", value: "Iceland"}, {label: "India", value: "India"},
      {label: "Indonesia", value: "Indonesia"}, {label: "Iran", value: "Iran"},
      {label: "Iraq", value: "Iraq"}, {label: "Ireland", value: "Ireland"},
      {label: "Israel", value: "Israel"}, {label: "Italy", value: "Italy"},
      {label: "Jamaica", value: "Jamaica"}, {label: "Japan", value: "Japan"},
      {label: "Jordan", value: "Jordan"}, {label: "Kazakhstan", value: "Kazakhstan"},
      {label: "Kenya", value: "Kenya"}, {label: "Korea, South", value: "Korea, South"},
      {label: "Kuwait", value: "Kuwait"}, {label: "Kyrgyzstan", value: "Kyrgyzstan"},
      {label: "Latvia", value: "Latvia"}, {label: "Lebanon", value: "Lebanon"},
      {label: "Liberia", value: "Liberia"}, {label: "Liechtenstein", value: "Liechtenstein"},
      {label: "Lithuania", value: "Lithuania"}, {label: "Luxembourg", value: "Luxembourg"},
      {label: "Madagascar", value: "Madagascar"}, {label: "Malaysia", value: "Malaysia"},
      {label: "Maldives", value: "Maldives"}, {label: "Malta", value: "Malta"},
      {label: "Mauritania", value: "Mauritania"}, {label: "Mauritius", value: "Mauritius"},
      {label: "Mexico", value: "Mexico"}, {label: "Moldova", value: "Moldova"},
      {label: "Monaco", value: "Monaco"}, {label: "Mongolia", value: "Mongolia"},
      {label: "Montenegro", value: "Montenegro"}, {label: "Morocco", value: "Morocco"},
      {label: "Namibia", value: "Namibia"}, {label: "Nepal", value: "Nepal"},
      {label: "Netherlands", value: "Netherlands"}, {label: "New Zealand", value: "New Zealand"},
      {label: "Nicaragua", value: "Nicaragua"}, {label: "Niger", value: "Niger"},
      {label: "Nigeria", value: "Nigeria"}, {label: "North Macedonia", value: "North Macedonia"},
      {label: "Norway", value: "Norway"}, {label: "Oman", value: "Oman"},
      {label: "Pakistan", value: "Pakistan"}, {label: "Panama", value: "Panama"},
      {label: "Papua New Guinea", value: "Papua New Guinea"}, {label: "Paraguay", value: "Paraguay"},
      {label: "Peru", value: "Peru"}, {label: "PhilippineVenezuelas", value: "Philippines"},
      {label: "Poland", value: "Poland"}, {label: "Portugal", value: "Portugal"},
      {label: "Qatar", value: "Qatar"}, {label: "Romania", value: "Romania"},
      {label: "Russia", value: "Russia"}, {label: "Rwanda", value: "Rwanda"},
      {label: "Saint Lucia", value: "Saint Lucia"},
      {label: "Saint Vincent and the Grenadines", value: "Saint Vincent and the Grenadines"},
      {label: "San Marino", value: "San Marino"}, {label: "Saudi Arabia", value: "Saudi Arabia"},
      {label: "Senegal", value: "Senegal"}, {label: "Serbia", value: "Serbia"},
      {label: "Seychelles", value: "Seychelles"}, {label: "Singapore", value: "Singapore"},
      {label: "Slovakia", value: "Slovakia"}, {label: "Slovenia", value: "Slovenia"},
      {label: "Somalia", value: "Somalia"}, {label: "South Africa", value: "South Africa"},
      {label: "Spain", value: "Spain"}, {label: "Sri Lanka", value: "Sri Lanka"},
      {label: "Sudan", value: "Sudan"}, {label: "Suriname", value: "Suriname"},
      {label: "Sweden", value: "Sweden"}, {label: "Switzerland", value: "Switzerland"},
      {label: "Taiwan*", value: "Taiwan*"}, {label: "Tanzania", value: "Tanzania"},
      {label: "Thailand", value: "Thailand"}, {label: "Togo", value: "Togo"},
      {label: "Trinidad and Tobago", value: "Trinidad and Tobago"},
      {label: "Tunisia", value: "Tunisia"}, {label: "Turkey", value: "Turkey"},
      {label: "Uganda", value: "Uganda"}, {label: "Ukraine", value: "Ukraine"},
      {label: "United Arab Emirates", value: "United Arab Emirates"},
      {label: "United Kingdom", value: "United Kingdom"}, {label: "Uruguay", value: "Uruguay"},
      {label: "US", value: "US"}, {label: "Uzbekistan", value: "Uzbekistan"},
      {label: "Venezuela", value: "Venezuela"}, {label: "Vietnam", value: "Vietnam"},
      {label: "Zambia", value: "Zambia"}, {label: "Zimbabwe", value: "Zimbabwe"},
      {label: "Dominica", value: "Dominica"}, {label: "Grenada", value: "Grenada"},
      {label: "Mozambique", value: "Mozambique"}, {label: "Syria", value: "Syria"},
      {label: "Timor-Leste", value: "Timor-Leste"}, {label: "Belize", value: "Belize"},
      {label: "Laos", value: "Laos"}, {label: "Libya", value: "Libya"},
      {label: "West Bank and Gaza", value: "West Bank and Gaza"},
      {label: "Guinea-Bissau", value: "Guinea-Bissau"}, {label: "Mali", value: "Mali"},
      {label: "Saint Kitts and Nevis", value: "Saint Kitts and Nevis"}, {label: "Kosovo", value: "Kosovo"},
      {label: "Burma", value: "Burma"}, {label: "MS Zaandam", value: "MS Zaandam"},
      {label: "Botswana", value: "Botswana"}, {label: "Burundi", value: "Burundi"},
      {label: "Sierra Leone", value: "Sierra Leone"}, {label: "Malawi", value: "Malawi"},
      {label: "South Sudan", value: "South Sudan"}, {label: "Western Sahara", value: "Western Sahara"},
      {label: "Sao Tome and Principe", value: "Sao Tome and Principe"}, {label: "Yemen", value: "Yemen"}
    ];
    this.paisElegido = 'Venezuela'
  }
}

@Component({
  selector: 'app-sir002',
  templateUrl: './sir002.component.html',
  styleUrls: ['./sir002.component.css']
})
export class Sir002Component implements OnInit {
  sir02Data: SIR02Data;
  blockedPnlSIR02: boolean = false;
  baseApiUrl = environment.baseApiUrl;

  constructor(private httpClient: HttpClient, private datePipe: DatePipe) {
    this.sir02Data = new SIR02Data;
  }

  ngOnInit(): void {

  }

  updateModel() {
    this.blockedPnlSIR02 = true;
    this.sir02Data.fi = this.datePipe.transform(this.sir02Data.date, 'M/d/yy');
    this.httpClient.get<any>(`${this.baseApiUrl}/sir02?country=${this.sir02Data.paisElegido}&fi=${this.sir02Data.fi}&rp=${this.sir02Data.rp}&i0=${this.sir02Data.i0}&s0=${this.sir02Data.s0}&r0=${this.sir02Data.r0}`).subscribe((data: JSON) => {
         this.sir02Data.modData = {
            labels: data['data']['data'][0],
            datasets: [
                {
                    label: data['data']['index'][4],
                    data: data['data']['data'][4],
                    fill: false,
                    borderColor: '#00ff00'
                },
                {
                    label: data['data']['index'][5],
                    data: data['data']['data'][5],
                    fill: false,
                    borderColor: '#0000ff'
                },
                {
                    label: data['data']['index'][6],
                    data: data['data']['data'][6],
                    fill: false,
                    borderColor: '#21AB13'
                }
           ]
        }
        this.sir02Data.modDataInf = {
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
                    borderColor: '#a52714'
                },
                {
                    label: data['data']['index'][3],
                    data: data['data']['data'][3],
                    fill: false,
                    borderColor: '#ff0000'
                },
            ]
        }
        this.blockedPnlSIR02 = false;
      },
      error => this.blockedPnlSIR02 = false);
  }

}
