import { Injectable } from '@angular/core';
import {Annotation} from '../table/annotation';
import {Observable, of, Subject, BehaviorSubject} from 'rxjs';
import * as _ from 'lodash';

@Injectable({
  providedIn: 'root'
})

export class DataService {

  private ANNOTATION_DATA = new BehaviorSubject<Annotation[]>([]);

  public getAnnotationData(): Observable<Annotation[]> {
    return this.ANNOTATION_DATA.asObservable();
  }

  public getAnnotations(){
    return this.ANNOTATION_DATA.getValue();
  }

  public addRow(row: Annotation){
    this.ANNOTATION_DATA.getValue().push(row);
    this.ANNOTATION_DATA.next(this.ANNOTATION_DATA.getValue());
  }

  public removeRow(id) {
    _.remove(this.ANNOTATION_DATA.getValue(), obj => obj.cid === id);
    this.ANNOTATION_DATA.next(this.ANNOTATION_DATA.getValue());
  }

  public removeAll() {
    console.log(this.ANNOTATION_DATA.getValue());
    _.forEach(this.ANNOTATION_DATA.getValue(), (item: Annotation, inx) => {
      this.ANNOTATION_DATA.getValue().splice(0, 1);
    });
    this.ANNOTATION_DATA.next(this.ANNOTATION_DATA.getValue());
  }

  public refresh() {
    this.ANNOTATION_DATA.next(this.ANNOTATION_DATA.getValue());
  }

  getLastId() {
    let max = 0;
    _.forEach(this.ANNOTATION_DATA.getValue(), (item: Annotation, inx) => {
      if (item.cid > max)
        max = item.cid;
    });
    return max;
  }

  reset(){
    this.ANNOTATION_DATA = new BehaviorSubject<Annotation[]>([]);
  }

}
