import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {SuccessComponent} from './pages/success/success.component';
import {TaskComponent} from './pages/task/task.component';
import {StartComponent} from './pages/start/start.component';


const routes: Routes = [
  { path: 'start', component: StartComponent },
  { path: 'task', component: TaskComponent },
  { path: 'success/:id', component: SuccessComponent },
  { path: '', redirectTo: '/start', pathMatch: 'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
