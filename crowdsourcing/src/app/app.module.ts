import { BrowserModule } from '@angular/platform-browser';
import {CUSTOM_ELEMENTS_SCHEMA, NgModule} from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LabelComponent } from './label/label.component';
import { ImageComponent } from './image/image.component';
import {FormsModule} from '@angular/forms';
import {MaterialModule} from './material.module';
import {DialogComponent} from './dialog/dialog.component';
import {TableComponent} from './table/table.component';
import {HttpClientModule} from '@angular/common/http';
import {SuccessComponent} from './pages/success/success.component';
import {TaskComponent} from './pages/task/task.component';
import {StartComponent} from './pages/start/start.component';
import {EvaluationComponent} from './pages/evaluation/evaluation.component';

@NgModule({
  declarations: [
    AppComponent,
    LabelComponent,
    ImageComponent,
    DialogComponent,
    TableComponent,
    StartComponent,
    TaskComponent,
    SuccessComponent,
    EvaluationComponent
  ],
  imports: [
    FormsModule,
    HttpClientModule,
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule
  ],
  schemas: [ CUSTOM_ELEMENTS_SCHEMA ],
  providers: [],
  entryComponents: [DialogComponent],
  bootstrap: [AppComponent]
})
export class AppModule { }
