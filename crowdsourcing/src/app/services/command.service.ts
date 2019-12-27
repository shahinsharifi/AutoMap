import { Injectable } from '@angular/core';
import {environment} from '../../environments/environment';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CommandService {

  baseUrl = environment.baseURL;
  appContext = environment.context;
  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'cache-control': 'no-cache',
      'Accept': 'application/json'
    })
  };

  constructor(private http: HttpClient) {}


  public execute(cmd: string, method: string, responseType: string, data: any, isRemoteServer: boolean) {
    let url = '';
    if (isRemoteServer)
      url = this.baseUrl + '/' + this.appContext + '/' + cmd + '/';
    else
      url = cmd;
    if (method.toLocaleLowerCase() === 'post') {
      if (responseType.toLocaleLowerCase() === 'blob')
        return this.doBinaryDownload(url, data);
      else
        return this.doPostCall(url, data)
    } else
      return this.doGetCall(url);
  }


  private doGetCall(url: string) {
    return this.http.get(url);
  }


  private doPostCall(url: string, data: any) {
    return this.http.post<any>(url, data, this.httpOptions);
  }


  private doBinaryDownload(url: string, data: any): Observable<Blob> {
    return this.http.post(url, data, {headers: this.httpOptions.headers, responseType: 'blob'});
  }
}
