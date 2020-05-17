import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from "@angular/common/http";
import { DatePipe } from '@angular/common';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TableModule } from 'primeng/table';
import { ChartModule } from 'primeng/chart';
import { ToastModule } from "primeng/toast";
import { SpinnerModule } from 'primeng/spinner';
import { FormsModule } from '@angular/forms';
import { BlockUIModule } from 'primeng/blockui';
import { PanelModule } from 'primeng/panel';
import { ButtonModule } from 'primeng/button';
import { DropdownModule } from 'primeng/dropdown';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { CalendarModule } from 'primeng/calendar';
import { Sir001Component } from './sir001/sir001.component';
import { ModsComponent } from './mods/mods.component';
import { Sir002Component } from './sir002/sir002.component';
import { Seir001Component } from './seir001/seir001.component';

@NgModule({
  declarations: [
    AppComponent,
    Sir001Component,
    ModsComponent,
    Sir002Component,
    Seir001Component,
  ],
  imports: [
    CommonModule,
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    TableModule,
    ChartModule,
    ToastModule,
    SpinnerModule,
    FormsModule,
    BlockUIModule,
    PanelModule,
    ButtonModule,
    DropdownModule,
    ProgressSpinnerModule,
    CalendarModule,
  ],
  providers: [DatePipe],
  bootstrap: [AppComponent]
})
export class AppModule { }
