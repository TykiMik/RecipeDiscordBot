import {NgModule} from '@angular/core';
import {MatNativeDateModule} from '@angular/material/core';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatTableModule} from '@angular/material/table';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';

@NgModule({
  exports: [
    MatNativeDateModule,
    MatPaginatorModule,
    MatProgressSpinnerModule,
    MatTableModule,
    MatCheckboxModule,
    MatButtonModule,
    MatIconModule
  ]
})
export class MaterialModule {}
