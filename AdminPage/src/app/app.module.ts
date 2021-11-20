import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule} from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RecipeListComponent } from './recipe-list/recipe-list.component';
import { MaterialModule } from 'src/material.module';
import { LoginPageComponent } from './login-page/login-page.component';

import { AuthInterceptorService } from './auth-interceptor/auth-interceptor.service';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { ControlPanelComponent } from './control-panel/control-panel.component';
import { BannedUsersListComponent } from './banned-users-list/banned-users-list.component';

@NgModule({
  declarations: [
    AppComponent,
    RecipeListComponent,
    LoginPageComponent,
    ControlPanelComponent,
    BannedUsersListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptorService,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
