import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

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

@NgModule({
  declarations: [
    AppComponent,
    LabelComponent,
    ImageComponent,
    DialogComponent,
    TableComponent,
    TaskComponent,
    SuccessComponent
  ],
  imports: [
    FormsModule,
    HttpClientModule,
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule
  ],
  providers: [],
  entryComponents: [DialogComponent],
  bootstrap: [AppComponent]
})
export class AppModule { }
