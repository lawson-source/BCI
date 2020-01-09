import {Component, OnInit} from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent implements OnInit  {
  // tslint:disable-next-line:max-line-length
   public graph: any ;
   constructor(private http: HttpClient) {

  }
  ngOnInit(): void {
     const headers = new HttpHeaders().set('Content-Type', 'application/json');
     const params = {start_date: '2019-09-10', end_date: '2019-09-31'};
     this.http.post('http://localhost:8080/scatter', params, {headers},
      ).subscribe(data => {
      console.log(data);
      this.graph = data;
    });
           }
      }
