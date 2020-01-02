import {Component, Input, OnChanges, OnInit, ViewChild, ViewEncapsulation, SimpleChanges, Output, EventEmitter} from '@angular/core';
import {environment} from '../../environments/environment';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {DialogComponent} from "../dialog/dialog.component";
import {DataService} from '../services/data.service';
import * as _ from 'lodash';
import {Bbox} from './bbox';
import {Annotation} from '../table/annotation';
import {CommandService} from '../services/command.service';
import {ActivatedRoute, Router} from '@angular/router';
import {TimeService} from '../services/time.service';
import {UserService} from '../services/user.service';

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class ImageComponent implements OnInit, OnChanges {

  drag = false;
  startX: number = null;
  startY: number = null;
  userId: String;
  currentImageId: number;
  predictionCount: number;
  baseImage = new Image();
  drawingImage = new Image();
  currentBbox: Bbox = null;
  currentAnnotation: Annotation;
  drawingContext: CanvasRenderingContext2D = null;

  @Input('width') width: number;
  @Input('active-annotation') activeAnnotation: boolean;
  @Input('next-row') next: number;
  @Input('evaluation-mode') evaluationMode: boolean;
  @Output('onAnnotationModeChanged') onAnnotationModeChanged = new EventEmitter();
  @Output('onTaskLoaded') onTaskLoaded = new EventEmitter();
  @ViewChild('wrapper', {static: true}) wrapper;
  @ViewChild('imageContainer', {static: true}) myCanvas;

  constructor(public dialog: MatDialog, private dataService: DataService, private command: CommandService, private router: Router,
              private route: ActivatedRoute, private time: TimeService, private userService: UserService) {}

  ngOnInit() {
    this.nextRow();
    this.refresh();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.activeAnnotation) {
      if (changes.activeAnnotation.currentValue) {
        this.time.init();
      } else {
        this.time.stopTimeRecording();
      }
    }else if(changes.next){
      this.nextRow();
    }
  }

  nextRow() {
    if (!this.evaluationMode) {
      this.loadTask(this.userService.getUserId()).subscribe((task) => {
        if (task && task.status == 'ok') {
          this.currentImageId = task['id'];
          this.predictionCount = task['prediction'];
          let url = environment.baseURL + '/' + environment.context + '/image/' + task['image_name'];
          this.baseImage.src = url;
          this.drawingImage = _.cloneDeep(this.baseImage);
          this.baseImage.onload = () => {
            let context = this.myCanvas.nativeElement.getContext('2d');
            const w = this.baseImage.width;
            const h = this.baseImage.height;
            context.canvas.width = w;
            context.canvas.height = h;
            this.render(context, this.baseImage, context.canvas.width, context.canvas.height);
          };
          this.onTaskLoaded.emit(true);
        } else {
          this.onTaskLoaded.emit(false);
        }
      });
    } else {
      this.dataService.removeAll();
      this.loadAnnotation().subscribe((response) => {
        if (response && response.status == 'ok') {
          let image = response.image.name;
          let url = environment.baseURL + '/' + environment.context + '/image/' + image;
          this.baseImage.src = url;
          this.baseImage.onload = () => {
            let context = this.myCanvas.nativeElement.getContext('2d');
            const w = this.baseImage.width;
            const h = this.baseImage.height;
            context.canvas.width = w;
            context.canvas.height = h;
            this.render(context, this.baseImage, context.canvas.width, context.canvas.height);
            let annotations = response.annotations;
            let labels = response.labels;
            for (let i = 0; i < annotations.length; i++) {
              annotations[i].cid = annotations[i].id;
              annotations[i].labelName = labels[String(annotations[i].id)];
              this.dataService.addRow(annotations[i]);
            }
          };
        }
      });
    }
  }

  loadTask(userId: String) {
    const cmd = 'task/get/' + userId;
    return this.command.execute(cmd, 'GET', 'json', {}, true);
  }

   loadAnnotation() {
    const cmd = 'annotation/get';
    return this.command.execute(cmd, 'GET', 'json', {}, true);
  }

  mouseDownEvent(e) {
    if (this.activeAnnotation) {
      this.startX = e.clientX;
      this.startY = e.clientY;
      this.drag = true;
      this.drawingContext = this.myCanvas.nativeElement.getContext('2d');
    }
  }

  mouseMoveEvent(e) {
    if (this.activeAnnotation && this.drag) {
      const sx = this.startX;
      const sy = this.startY;

      const canvasTop = this.myCanvas.nativeElement.getBoundingClientRect().top;
      const canvasLeft = this.myCanvas.nativeElement.getBoundingClientRect().left;
      const canvasWidth = this.myCanvas.nativeElement.getBoundingClientRect().width;
      const canvasHeight = this.myCanvas.nativeElement.getBoundingClientRect().height;
      this.render(this.drawingContext, this.baseImage, canvasWidth, canvasHeight);

      const x = sx - canvasLeft;
      const y = sy - canvasTop;
      const w = e.clientX - canvasLeft - x;
      const h = e.clientY - canvasTop - y;
      this.draw(this.drawingContext, x, y, w, h);
      this.currentBbox = new Bbox(y, x, y + h, x + w);
    }
  }

  mouseUpEvent(e) {
    if (this.activeAnnotation) {
      this.drag = false;
      this.drawingContext = null;
      this.openDialog();
    }
  }

  erase(context, canvasWidth, canvasHeight) {
    context.clearRect(0, 0, canvasWidth, canvasHeight)
  }

  draw(context, x, y, w, h): CanvasRenderingContext2D {
    context.beginPath();
    context.strokeStyle = 'red';
    context.lineWidth = 5;
    context.rect(x, y, w, h);
    context.stroke();
    return context;
  }

  render(context, baseImage, canvasWidth, canvasHeight) {
    let scale = Math.min(context.canvas.width / baseImage.width, context.canvas.height / baseImage.height);
    let x = (context.canvas.width / 2) - (baseImage.width / 2) * scale;
    let y = (context.canvas.height / 2) - (baseImage.height / 2) * scale;
    context.drawImage(baseImage, x, y, baseImage.width * scale, baseImage.height * scale);
  }

  openDialog() {
    const dialogRef = this.dialog.open(DialogComponent, {
      width: '450px'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result && result != '') {
        this.currentAnnotation = new Annotation();
        this.currentAnnotation.cid = this.dataService.getLastId() + 1;
        this.currentAnnotation.labelId = result.id;
        this.currentAnnotation.imageId = this.currentImageId;
        this.currentAnnotation.userId = this.userService.getUserId();
        this.currentAnnotation.labelName = result.name;
        this.currentAnnotation.top = this.currentBbox.top;
        this.currentAnnotation.left = this.currentBbox.left;
        this.currentAnnotation.bottom = this.currentBbox.bottom;
        this.currentAnnotation.right = this.currentBbox.right;
        this.currentAnnotation.timeEffort = Number(this.time.getTimeOnPage());
        this.dataService.addRow(this.currentAnnotation);
      } else {
        this.dataService.refresh();
      }
      this.time.stopTimeRecording();
    });
  }

  refresh() {
    this.dataService.getAnnotationData().subscribe((annotations: Annotation[]) => {
      let annotation: Annotation;
      let context = this.myCanvas.nativeElement.getContext('2d');
      const canvasWidth = this.myCanvas.nativeElement.getBoundingClientRect().width;
      const canvasHeight = this.myCanvas.nativeElement.getBoundingClientRect().height;
      this.render(context, this.baseImage, canvasWidth, canvasHeight);
      for (let i = 0; i < annotations.length; i++) {
        annotation = annotations[i];
        let x = annotation.left;
        let y = annotation.top;
        let w = annotation.right - annotation.left;
        let h = annotation.bottom - annotation.top;
        this.draw(context, x, y, w, h);
      }
    });
  }

}
