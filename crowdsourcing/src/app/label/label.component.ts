import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {Label} from './label';
import {FormControl, Validators} from '@angular/forms';
import {CommandService} from '../services/command.service';

@Component({
  selector: 'app-label',
  templateUrl: './label.component.html',
  styleUrls: ['./label.component.scss']
})
export class LabelComponent implements OnInit {

  labels: Label[] = [];

  formControl = new FormControl('');
  @Output() labelSelected = new EventEmitter<Label>();


  constructor(private commandService: CommandService) {}

  ngOnInit() {
    this.loadLabels().subscribe((labels) => {
      this.labels = labels;
      this.onChange();
    });
  }

  loadLabels(){
    const cmd = 'labels/all';
    return this.commandService.execute(cmd, 'GET', 'json', {}, true);
  }

  onChange(){
    this.formControl.valueChanges.subscribe(value => {
      this.labelSelected.emit(value);
    });
  }

}
