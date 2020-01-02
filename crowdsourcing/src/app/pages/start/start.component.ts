import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {UserService} from '../../services/user.service';

@Component({
  selector: 'app-start',
  templateUrl: './start.component.html',
  styleUrls: ['./start.component.scss']
})
export class StartComponent implements OnInit {

  private userId:String;

  constructor(private route: ActivatedRoute, private router: Router, private userService: UserService) { }

  ngOnInit() {
    /*this.route.queryParams.subscribe(params => {
      this.userId = params.uid;
    });*/
  }

  start() {
    this.router.navigate([
      (this.userId) ? ('task?uid=' + this.userId) : 'task/'
    ]);
  }

}
