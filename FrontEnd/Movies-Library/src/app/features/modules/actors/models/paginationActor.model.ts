
import {ActorModel} from "./Actor.model";

export interface PaginationActorModel{
  dates?: Object;
  page: number;
  results: Array<ActorModel>;
  total_pages: number;
  total_results: number;
}
