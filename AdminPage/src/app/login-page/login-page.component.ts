import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss']
})
export class LoginPageComponent implements OnInit {
  public loginInvalid = false;
  private formSubmitAttempt = false;
  form: FormGroup;


  constructor(private fb: FormBuilder, private _authService: AuthService, private router: Router) { 
    this.form = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    if (this._authService.isLoggedIn())
    {
      this.router.navigate(['controlpanel'])
    }
  }

  onSubmit()
  {
    this.loginInvalid = false;
    this.formSubmitAttempt = false;
    if (this.form.valid) {
      try {
        const username = this.form.get('username')?.value;
        const password = this.form.get('password')?.value;
        this._authService.Login(username, password).subscribe(
          user => 
          {
            this._authService.setSession(user);
            this.router.navigate(['controlpanel']);
          },
          _ => this.loginInvalid = true
        );
      } catch (err) {
        this.loginInvalid = true;
      }
    } else {
      this.formSubmitAttempt = true;
    }
  }

}
