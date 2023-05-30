import {Component, OnInit, ViewChild} from '@angular/core';
import {User} from "../../../../../authentication/models/User";
import {AdminService} from "../../../../services/admin.service";
import {MatTableDataSource, MatTableDataSourcePaginator} from "@angular/material/table";
import {MatSort} from "@angular/material/sort";

@Component({
  selector: 'app-manage-users',
  templateUrl: './manage-users.component.html',
  styleUrls: ['./manage-users.component.scss']
})
export class ManageUsersComponent implements OnInit {
  public dataSource!: MatTableDataSource<User, MatTableDataSourcePaginator>;
  public displayedColumns: string[] = ['id', 'email', 'lastname', 'firstname', 'changePassword', 'isStaff', 'isAdmin'];

  @ViewChild(MatSort, { static: true }) sort!: MatSort;

  constructor(private adminService: AdminService) {
  }



  ngOnInit() {
    this.adminService.getUsers().subscribe((res: any) => {
      let temp:any = [];
      for (let simpleRes of res) {
        temp.push({
          id: simpleRes.id,
          email: simpleRes.email,
          last_name: simpleRes.last_name,
          first_name: simpleRes.first_name,
          roles: {
            admin: simpleRes.is_superuser,
            staff: simpleRes.is_staff,
            user: true
          }
        });
      }
      this.dataSource = new MatTableDataSource<User, MatTableDataSourcePaginator>(temp);
    });
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

}
