import {Bbox} from '../image/bbox';
import {Label} from '../label/label';

export class Annotation {
  public cid: number;
  public top: number;
  public left: number;
  public bottom: number;
  public right: number;
  public labelId: number;
  public labelName: String;
  public imageId: number;
  public userId: String;
  public timeEffort: number
}
