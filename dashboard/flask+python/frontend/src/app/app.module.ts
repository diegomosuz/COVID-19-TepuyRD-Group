import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from "@angular/common/http";

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TableModule } from 'primeng/table';
import { ChartModule } from 'primeng/chart';
import { ToastModule } from "primeng/toast";

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    TableModule,
    ChartModule,
    ToastModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
