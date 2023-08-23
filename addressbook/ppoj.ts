import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-contacts',
  templateUrl: './contacts.upload.html',
  styleUrls: ['./contacts.styles.css']
})
export class ContactsComponent implements OnInit {

  contacts: any[] = [];
  newContact: any = {};

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.getContacts();
  }

  getContacts() {
    this.http.get('/contacts').subscribe((data: any) => {
      this.contacts = data;
    });
  }

  addContact() {
    this.http.post('/contacts', this.newContact).subscribe((data: any) => {
      this.contacts.push(data);
      this.newContact = {};
    });
  }

  updateContact(contact: any) {
    this.http.put(`/contacts/${contact.id}`, contact).subscribe();
  }

  deleteContact(contact: any) {
    this.http.delete(`/contacts/${contact.id}`).subscribe(() => {
      this.contacts = this.contacts.filter(c => c.id !== contact.id);
    });
  }

}
