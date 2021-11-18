import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { HttpErrorResponse, HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { catchError, retry } from 'rxjs/operators';

export interface RecipeResponse {
  items: Recipe[];
  total_count: number;
}


export interface Recipe {
  id: string;
  creator: string;
  creator_id: bigint;
  name: string;
  content: string;
  tags: string[];
  request_count: number;
  rating: number;
  creation_date: Date;
}


@Injectable({ providedIn: 'root' })
export class RecipeApiService {
  apiURL = 'http://192.168.0.241:5000/api/recipes';

  constructor(private http: HttpClient) { }

  getRecipes(page: number, per_page: number = 30, recipeNameFilter: string = "", creatorFilter: string = "", creatorIdFilter: string = "") {
    let params: HttpParams = new HttpParams()
      .set('page', page+1)
      .set('per_page', per_page);
    

    if (recipeNameFilter)
    {
      params = params.set('recipe_name', recipeNameFilter)
    }
    if (creatorFilter)
    {
      params = params.set('creator', creatorFilter)
    }
    if (creatorIdFilter)
    {
      params = params.set('creator_id', creatorIdFilter)
    }
    const options = { 
      params: params
    }; 
    return this.http.get<RecipeResponse>(this.apiURL, options)
      .pipe(
        retry(2),
        catchError(this.handleError)
      );
  }

  deleteRecipes(ids: string[]){
    const options = {
      body: {
        items: ids
      },
    };
    return this.http.delete<RecipeResponse>(this.apiURL,options)
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
