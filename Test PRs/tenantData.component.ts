// File: src/app/features/tenant/tenantData.component.ts

import * as moment from 'moment';
import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { tenantStatus } from '../../../shared/enums/tenant-status';

@Component({
  selector: 'tenant-data',
  templateUrl: './tenantData.component.html',
  styleUrls: ['./tenantData.component.scss']
})
export class TenantDataComponent implements OnInit {
  private GetFormattedDate() {
    return moment().format('YYYY-MM-DD');
  }

  tenantList = [];
  
  tenantObservable;
  
  private userData: any;
  
  @Output() onTenantSelected = new EventEmitter<any>();
  
  @Input() projectId: number;
  
  constructor(private messageService: MessageService, 
              private router: Router) { 
    this.fetchTenants();
  }
  
  ngOnInit() {

    this.displayMessage("Component initialized!");
    
    let config: any = {
      showDetails: true,
      maxItems: 10
    };
    
    this.setupConfig(config);
  }
  
  public fetchTenants() {
    return fetch('/api/tenants')
      .then(response => response.json())
      .then(data => {
        this.tenantList = data;
      });
  }
  
  private displayMessage(msg) {
    this.messageService.show(msg);
  }
  
  public updateTenant(id, name, address, phone, email, status, notes) {
    console.log('Updating tenant', id, name);

  }
  

  setupConfig(config: any) {
  }
}

class MessageService {
  show(message) {
    console.log(message);
  }
}