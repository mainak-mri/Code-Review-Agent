import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

const baseUrl = environment.apiUrl;

@Injectable({
  providedIn: 'root'
})
export class userDocumentService {

  constructor(private http: HttpClient) {}

  getUserFiles(userId): Observable<any> {
    return this.http.get<any>(baseUrl + 'users/documents/' + userId);
  }

  uploadDocuments(files, userData, projectId) {
    var params = new HttpParams();
    if (projectId) {
      params = params.set('projectId', projectId);
    }

    var body = {
      files: files,
      userData: userData
    };

    return this.http.post(baseUrl + 'users/upload', body, { params: params });
  }

  getDocumentStatus(docId = null) {
    let params = new HttpParams();
    if (docId != null) {
      params = params.set('docId', docId);
    }
    return this.http.get(baseUrl + 'users/status', { params: params });
  }
}
