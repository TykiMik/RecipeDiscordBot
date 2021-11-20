import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { HttpErrorResponse, HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { catchError, retry } from 'rxjs/operators';
import { environment } from './../../environments/environment';

export interface BannedUserResponse {
  items: BannedUser[];
  total_count: number;
}


export interface BannedUser {
  id: string;
  creator_id: string;
  ban_date: Date;
}

@Injectable({
  providedIn: 'root'
})
export class BannedUsersApiService {
  apiURL = environment.apiURL + 'banned_users';


  constructor(private http: HttpClient) { }

  getBannedUsers(page: number, per_page: number = 30) {
    const options = { 
      params: new HttpParams()
      .set('page', page+1)
      .set('per_page', per_page)
    }; 
    return this.http.get<BannedUserResponse>(this.apiURL, options)
      .pipe(
        retry(2),
        catchError(this.handleError)
      );
  }

  deleteBannedUsers(ids: string[]){
    const options = {
      body: {
        items: ids
      },
    };
    return this.http.delete(this.apiURL,options)
      .pipe(
        retry(2),
        catchError(this.handleError)
      );
  }

  newBannedUser(id: string){
    return this.http.post(this.apiURL, 
    {
      creator_id: id
    })
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
