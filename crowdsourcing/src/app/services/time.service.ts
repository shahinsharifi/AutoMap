import { Injectable } from '@angular/core';
import * as TimeMe from 'timeme.js'

@Injectable({
  providedIn: 'root'
})
export class TimeService {

  constructor() {
    this.init();
  }

  init() {
    TimeMe.initialize({
      currentPageName: "my-home-page",
      idleTimeoutInSeconds: 1,
    });
  }

  getTimeOnPage(): number{
    let timeSpentOnPage = TimeMe.getTimeOnCurrentPageInSeconds();
    return timeSpentOnPage.toFixed(2);
  }

  startRecordingOnElement(element: String) {
    TimeMe.trackTimeOnElement(element);
  }

  getTimeOnElement(element: String): number {
    let timeSpentOnElement = TimeMe.getTimeOnElementInSeconds(element);
    return (timeSpentOnElement) ? timeSpentOnElement.toFixed(2) : 0;
  }

  stopTimeRecording() {
    TimeMe.resetAllRecordedPageTimes();
  }
}
