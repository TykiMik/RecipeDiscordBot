import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { HttpErrorResponse, HttpClient } from '@angular/common/http';
import { catchError, retry } from 'rxjs/operators';
import { environment } from './../../environments/environment';

export interface AdminResponse {
  items: Admin[];
}


export interface Admin {
  name: string;
}


@Injectable({
  providedIn: 'root'
})
export class RegisterApiService {
  apiURL = environment.apiURL + 'auth/register';


  constructor(private http: HttpClient) { }

  getAdmins() {
    return this.http.get<AdminResponse>(this.apiURL)
      .pipe(
        retry(2),
        catchError(this.handleError)
      );
  }

  deleteCurrentAdmin(){
    return this.http.delete(this.apiURL)
      .pipe(
        retry(2),
        catchError(this.handleError)
      );
  }

  newAdminUser(name: string, password: string){
    return this.http.post(this.apiURL, 
    {
      name: name,
      password: password
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
