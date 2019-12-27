import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {SuccessComponent} from './pages/success/success.component';
import {TaskComponent} from './pages/task/task.component';


const routes: Routes = [
  { path: 'task', component: TaskComponent },
  { path: 'success/:id', component: SuccessComponent },
  { path: '', redirectTo: '/task', pathMatch: 'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
