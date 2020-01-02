import {Component, Input, OnInit, ViewChild, ViewEncapsulation} from '@angular/core';
import {CommandService} from '../../services/command.service';
import {DataService} from '../../services/data.service';
import {ActivatedRoute, Router} from '@angular/router';
import * as _ from 'lodash';

@Component({
  selector: 'app-task',
  templateUrl: './task.component.html',
  styleUrls: ['./task.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class TaskComponent implements OnInit {

  width: number;
  activeAnnotation: boolean = false;
  isTaskAvailable: boolean;
  @ViewChild('parentElement', {static: true}) imageContainerParent;

  constructor(private commandService: CommandService, private dataService: DataService,
              private route: ActivatedRoute, private router: Router) {
  }

  ngOnInit() {
    this.dataService.reset();
    this.width = this.imageContainerParent.nativeElement.clientWidth;
  }

  toggleAnnotation() {
    this.activeAnnotation = true;
  }

  onAnnotationModeChanged(mode: boolean) {
    this.activeAnnotation = mode;
  }

  onTaskLoaded(flag) {
    this.isTaskAvailable = flag;
  }

  submitData() {
    const cmd = 'task/save';
    let annotations = this.dataService.getAnnotations();
    this.commandService.execute(cmd, 'POST', 'json', annotations, true).subscribe((response) => {
      this.router.navigate([
        'success/' + response.id
      ]);
    });
  }

}
