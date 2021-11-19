import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { HttpErrorResponse, HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { catchError, retry } from 'rxjs/operators';
import * as moment from "moment";


export interface User {
  token: string;
  expires_in: number;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  apiURL = 'http://192.168.66.118:5000/api/auth';

  constructor(private http: HttpClient) { }

  Login(name: string, password: string){
      return this.http.post<User>(this.apiURL + '/login', {name, password})
      .pipe(
        retry(2),
        catchError(this.handleError)
      )
  }

  setSession(authResult: User) {
    const expiresAt = moment().add(authResult.expires_in,'second');

    localStorage.setItem('id_token', authResult.token);
    localStorage.setItem("expires_at", JSON.stringify(expiresAt.valueOf()) );
  }

  public isLoggedIn() {
    return moment().isBefore(this.getExpiration());
  }

  isLoggedOut() {
    return !this.isLoggedIn();
  }

  private getExpiration() {
    const expiration = localStorage.getItem("expires_at");
    if (expiration) {
      const expiresAt = JSON.parse(expiration);
      return moment(expiresAt);
    }
    else {
      return moment(-1);
    }
  }

  logout() {
    localStorage.removeItem("id_token");
    localStorage.removeItem("expires_at");
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
