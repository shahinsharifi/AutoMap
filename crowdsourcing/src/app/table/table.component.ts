import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {Annotation} from './annotation';
import {DataService} from '../services/data.service';
import {MatTableDataSource} from '@angular/material';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class TableComponent implements OnInit{

  displayedColumns = ['id', 'type', 'bbox', 'effort' , 'action'];
  dataSource = new MatTableDataSource<Annotation>([]);

  constructor(private dataService: DataService){

  }

  ngOnInit() {
    this.refresh();
  }


  refresh() {
    this.dataService.getAnnotationData().subscribe((data: Annotation[]) => {
      this.dataSource.data = data;
    });
  }

  deleteRow(id){
   this.dataService.removeRow(id);
   this.refresh();
  }
}




