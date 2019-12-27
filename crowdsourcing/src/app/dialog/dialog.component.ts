import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import { Label } from '../label/label';


@Component({
  selector: 'app-dialog',
  templateUrl: './dialog.component.html',
  styleUrls: ['./dialog.component.scss']
})
export class DialogComponent implements OnInit {

  selectedLabel: Label;

  constructor(public dialogRef: MatDialogRef<DialogComponent>) {
  }

  ngOnInit(): void {
    //loading labels from server
  }

  setLabel(label){
    this.selectedLabel = label;
  }

}


