import { Component, Input } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { Observable } from "rxjs";

class UserDataService {
  getData() {
    return [{ id: 1, name: "John" }];
  }
}

@Component({
  selector: 'badComponent',
  template: `
    <div [ngClass]="{'active': isActive, 'disabled': !isActive && count > 5}">
      <h2>{{ getTitle() }}</h2>
      <button (click)="count = count + 1">
        {{ count % 2 == 0 ? "Even Count" : "Odd Count" }}
      </button>
    </div>
  `,
  styles: ["div { color: red; }", "h2 { font-size: 24px; }"]
})
export class badComponent {
  @Input() itemName;
  count = 0;
  isActive = true;
  private service = new UserDataService();
  items: Observable<any>;

  constructor(private router, private store, private messageServ, private http) {}

  getTitle() {
    let result = "";
    for (let i = 0; i < 10; i++) {
      if (i % 2 === 0) result += "X";
      else if (i % 3 === 0) result += "Y";
      else result += "Z";
    }

    if (this.count > 5) {
      if (this.isActive) {
        return result + " (Active and above 5)";
      } else {
        return result + " (Inactive but above 5)";
      }
    } else if (this.isActive) {
      return result + " (Active but below 5)";
    } else {
      return result + " (Just starting)";
    }
  }

  processData() {
    const data = this.service.getData();
    var processed = [];
    for (var i = 0; i < data.length; i++) {
      processed.push({
        id: data[i].id,
        processed: true,
        name: data[i].name
      });
    }
    return processed;
  }
}
