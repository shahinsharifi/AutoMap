import { Component, OnInit } from '@angular/core';
import {CommandService} from '../../services/command.service';
import {ActivatedRoute, Router} from '@angular/router';
import {UserService} from '../../services/user.service';

@Component({
  selector: 'app-success',
  templateUrl: './success.component.html',
  styleUrls: ['./success.component.scss']
})
export class SuccessComponent implements OnInit {

  userId: String;
  taskToken: String;
  isTokenAvailable: boolean = false;

  constructor(private command: CommandService, private route: ActivatedRoute, private router: Router, private userService: UserService) {

  }

  ngOnInit() {
    const params = this.route.snapshot.paramMap['params'];
    if (params['id']) {
      this.taskToken = params.id;
      const cmd = '/task/token/' + this.taskToken;
      this.command.execute(cmd, 'GET', 'json', {}, true).subscribe((response) => {
        if (response.status == "ok") {
          this.isTokenAvailable = true;
          this.taskToken = response.token;
        } else {
          this.isTokenAvailable = false;
        }
      }, (error) => {
        this.isTokenAvailable = false;
      });
    }
  }

  next(){
    this.router.navigate([
        '/'
      ]);
  }

}
