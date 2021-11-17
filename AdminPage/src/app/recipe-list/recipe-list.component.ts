import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { RecipeApiService, Recipe, RecipeResponse } from '../recipe-api-service/recipe-api.service';
import {MatPaginator} from '@angular/material/paginator';
import {of as observableOf} from 'rxjs';
import {catchError, map, startWith, switchMap} from 'rxjs/operators';

@Component({
  selector: 'app-recipe-list',
  templateUrl: './recipe-list.component.html',
  styleUrls: ['./recipe-list.component.scss']
})
export class RecipeListComponent implements AfterViewInit{
  displayedColumns: string[] = ['creator', 'recipe_name', 'creation_date', 'request_count'];
  recipes: Recipe[] = []

  isLoadingResults = true;
  resultsLength = 0;

  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;

  constructor(private _recipeService: RecipeApiService) { }
  ngAfterViewInit(): void {
    this.paginator!.page
      .pipe(
        startWith({}),
        switchMap(() => {
          this.isLoadingResults = true;
          return this._recipeService.getRecipes(
            this.paginator!.pageIndex,
          ).pipe(catchError(() => observableOf(null)));
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
      .subscribe(data => (this.recipes = data));
  }

}
