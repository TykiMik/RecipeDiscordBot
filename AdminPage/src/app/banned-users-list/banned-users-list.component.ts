import { Component, ViewChild, AfterViewInit } from '@angular/core';
import {MatPaginator} from '@angular/material/paginator';
import {of as observableOf} from 'rxjs';
import {catchError, map, startWith, switchMap} from 'rxjs/operators';
import {SelectionModel} from '@angular/cdk/collections';
import { BannedUsersApiService, BannedUser } from '../banned-users-api/banned-users-api.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-banned-users-list',
  templateUrl: './banned-users-list.component.html',
  styleUrls: ['./banned-users-list.component.scss']
})
export class BannedUsersListComponent  implements AfterViewInit{
  displayedColumns: string[] = ['select', 'user_id', 'ban_date'];
  banned_users: BannedUser[] = []

  isLoadingResults = true;
  resultsLength = 0;

  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;
  pageSizeOptions: number[] = [10,20,30,40,50,100,200,500];
  selection = new SelectionModel<BannedUser>(true, []);

  form: FormGroup;
  private formSubmitAttempt = false;

  constructor(private fb: FormBuilder, private _bannedUsersService: BannedUsersApiService) { 
    this.form = this.fb.group({
      user_id: ['', 
      Validators.required]
    });
  }

  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.banned_users.length;
    return numSelected === numRows;
  }

  masterToggle() {
    if (this.isAllSelected()) {
      this.selection.clear();
      return;
    }

    this.selection.select(...this.banned_users);
  }

  getData(){
    return this._bannedUsersService.getBannedUsers(
      this.paginator!.pageIndex,
      this.paginator!.pageSize)
  }

  ngAfterViewInit(): void {
    this.paginator!.page
      .pipe(
        startWith({}),
        switchMap(() => {
          this.isLoadingResults = true;
          return this.getData()
          .pipe(catchError(() => observableOf(null)));
        }),
        map(data => {
          // Flip flag to show that loading has finished.
          this.isLoadingResults = false;

          if (data === null) {
            return [];
          }

          this.resultsLength = data.total_count;
          return data.items;
        }),
      )
      .subscribe(data => (this.banned_users = data));
  }

  deleteSelected() {
    if (this.selection.hasValue())
    {
      this._bannedUsersService.deleteBannedUsers(this.selection.selected.map(user => user.id))
      .subscribe(() => {
        this.paginator!.page.emit();
        this.selection.clear();
      });
    }
  }

  banNewUser()
  {
    this.formSubmitAttempt = false;
    if (this.form.valid) {
        console.log("valid user id")
        const user_id = this.form.get('user_id')?.value;
        this._bannedUsersService.newBannedUser(user_id).subscribe(() => {
          this.paginator!.page.emit();
          this.selection.clear();
        });
    } else {
      console.log("not valid user id")
      this.formSubmitAttempt = true;
    }
  }

}
