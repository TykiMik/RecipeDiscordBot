import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { RecipeApiService, Recipe, RecipeResponse } from '../recipe-api-service/recipe-api.service';
import {MatPaginator} from '@angular/material/paginator';
import {of as observableOf} from 'rxjs';
import {catchError, map, startWith, switchMap} from 'rxjs/operators';
import {SelectionModel} from '@angular/cdk/collections';


@Component({
  selector: 'app-recipe-list',
  templateUrl: './recipe-list.component.html',
  styleUrls: ['./recipe-list.component.scss']
})
export class RecipeListComponent implements AfterViewInit{
  displayedColumns: string[] = ['select', 'creator', 'recipe_name', 'creation_date', 'request_count', 'rating'];
  recipes: Recipe[] = []

  isLoadingResults = true;
  resultsLength = 0;

  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;
  selection = new SelectionModel<Recipe>(true, []);

  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.recipes.length;
    return numSelected === numRows;
  }

  masterToggle() {
    if (this.isAllSelected()) {
      this.selection.clear();
      return;
    }

    this.selection.select(...this.recipes);
  }

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

  deleteSelected() {
    if (this.selection.hasValue())
    {
      this._recipeService.deleteRecipes(this.selection.selected.map(recipe => recipe.id))
      .subscribe(() => {
        this.paginator!.page.emit();
        this.selection.clear();
      });
    }
  }

}
