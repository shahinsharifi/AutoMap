import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private userID: String;

  constructor() { }

  setUserId(userId: String){
    this.userID = userId;
  }

  getUserId(): String{
    return this.userID;
  }
}
