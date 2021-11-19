import { Component } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-control-panel',
  templateUrl: './control-panel.component.html',
  styleUrls: ['./control-panel.component.scss']
})
export class ControlPanelComponent  {

  constructor(private _authService: AuthService, private router:Router) { }
  
  logout()
  {
    this._authService.logout();
    this.router.navigate(['login'])
  }
}
