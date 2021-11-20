import { Component, AfterViewInit } from '@angular/core';
import { map } from 'rxjs';
import { RegisterApiService, Admin } from '../register-api/register-api.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../auth/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin-users',
  templateUrl: './admin-users.component.html',
  styleUrls: ['./admin-users.component.scss']
})
export class AdminUsersComponent implements AfterViewInit {
  displayedColumns: string[] = ['name'];
  admin_users: Admin[] = []

  form: FormGroup;

  isLoadingResults = true;
  creationError = false;
  deletionError = false;
  constructor(
    private fb: FormBuilder, 
    private _registerService: RegisterApiService,
    private _authService: AuthService,
    private router: Router
    ) { 
    this.form = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  private loadData(){
    this.isLoadingResults = true;
    this._registerService.getAdmins()
    .pipe(map(response => {
      return response.items
    })).subscribe(admins => {
      this.admin_users = admins;
      this.isLoadingResults = false;
    })
  }

  ngAfterViewInit(): void {
    this.loadData();
  }

  newAdmin() {
    if (this.form.valid) {
        const username = this.form.get('username')?.value;
        const password = this.form.get('password')?.value;
        this._registerService.newAdminUser(username, password).subscribe(
          () => {
            this.loadData(); 
            this.form.reset()
          },
          _ => this.creationError = true
        );
    }
  }

  deleteCurrentuser() {
    this._registerService.deleteCurrentAdmin().subscribe(() => {
      this._authService.logout();
      this.router.navigate(['login'])
    },
    () => {
      this.deletionError = true;
    })
  }

}
