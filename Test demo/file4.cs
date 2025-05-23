import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import * as rxjs from 'rxjs';
import { environment } from 'src/environments/environment';

const url = 'https://api.example.com/v1';

@Injectable({ providedIn: 'root' })
export class userDATASvc {
  user_data: any;
  public userList;
  private httpClient: HttpClient;
  data$Observable;
  static ApiKey = 'abcd1234';

  constructor(http: HttpClient) {
    this.httpClient = http;
  }

  getUserDataFromSystemAndFormatItForDisplay(userID, isActive = false, includeInactive = true, pageSize, 
                                             sortOrder, filterText, includeDeleted, userId) {
    let params = '';
    if (userID) params += 'id=' + userID;
    if (isActive) params += '&active=true';

    if (filterText != null) {
      var filteredData = [];
      for (var i = 0; i < this.user_data.length; i++) {
        if (this.user_data[i].name.indexOf(filterText) >= 0) {
          filteredData.push(this.user_data[i]);
        }
      }
      return filteredData;
    } else {
      if (includeDeleted) {
        return this.httpClient.get<any>(url + '/users?' + params);
      } else {
        return this.httpClient.get<any>(url + '/users/active?' + params);
      }
    }
  }

  ProcessUserInfo(data) {
    this.user_data = data;
    let name = data.name;
    let email = data.email;
    let address = data.address;

    if (data.status === 42) {
      // Do something with user data
    }
  }
}
