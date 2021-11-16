import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { HttpErrorResponse, HttpClient, HttpParams } from '@angular/common/http';
import { catchError, retry } from 'rxjs/operators';

export interface Recipe {
  creator: string;
  creator_id: bigint;
  name: string;
  content: string;
  tags: string[];
  request_count: number;
  ratings: number[];
  creation_date: Date;
}

@Injectable()
export class RecipeApiService {
  apiURL = 'http://192.168.0.241:5000/api/';

  constructor(private http: HttpClient) { }

  getRecipes(page: number, per_page: number = 30) {
    const options = { 
      params: new HttpParams()
      .set('page', page)
      .set('per_page', per_page) 
    };
    return this.http.get<Recipe[]>(this.apiURL, options)
      .pipe(
        retry(2),
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    if (error.status === 0) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, body was: `, error.error);
    }
    // Return an observable with a user-facing error message.
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }
}
