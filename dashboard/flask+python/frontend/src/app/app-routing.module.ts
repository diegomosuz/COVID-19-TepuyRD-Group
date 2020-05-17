import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { Sir001Component } from './sir001/sir001.component';
import { Sir002Component } from './sir002/sir002.component';
import { Seir001Component } from './seir001/seir001.component';
import { ModsComponent } from './mods/mods.component';


const routes: Routes = [
  { path: '', component: ModsComponent },
  { path: 'covid19', component: ModsComponent },
  { path: 'covid19/sir001', component: Sir001Component },
  { path: 'covid19/sir002', component: Sir002Component },
  { path: 'covid19/seir001', component: Seir001Component },

  // otherwise redirect to home
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
