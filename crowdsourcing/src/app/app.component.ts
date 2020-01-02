import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {UserService} from './services/user.service';
import * as _ from 'lodash';
//declare let turkGetParam: any;


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class AppComponent implements OnInit{

  constructor(private route: ActivatedRoute, private userService: UserService) {

  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      if(params.uid) {
        const uid = params.uid;
        this.userService.setUserId(uid);
        console.log(this.userService.getUserId());
      }
    });
  }

}

