import {Component, OnInit, ViewChild, ViewEncapsulation} from '@angular/core';
import {CommandService} from '../../services/command.service';
import {DataService} from '../../services/data.service';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-evaluation',
  templateUrl: './evaluation.component.html',
  styleUrls: ['./evaluation.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class EvaluationComponent implements OnInit {

  width: number;
  rowIndex: number = 0;
  @ViewChild('parentElement', {static: true}) imageContainerParent;

  constructor(private commandService: CommandService, private dataService: DataService,
              private route: ActivatedRoute, private router: Router) {
  }

  ngOnInit() {
    this.width = this.imageContainerParent.nativeElement.clientWidth;
  }

  next(){
    this.rowIndex = this.rowIndex + 1;
  }

  submitData() {

  }
}
