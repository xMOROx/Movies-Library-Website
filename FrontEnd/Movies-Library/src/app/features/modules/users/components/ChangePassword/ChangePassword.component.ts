import {Component, Inject, OnInit} from '@angular/core';
import {FormBuilder, FormGroup} from "@angular/forms";
import {AuthService} from "../../../../../authentication/services/auth.service";
import {Router} from "@angular/router";
import {ValidateService} from "../../../../../core/services/validate.service";
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {HttpErrorResponse} from "@angular/common/http";

@Component({
  selector: 'app-ChangePassword',
  templateUrl: './ChangePassword.component.html',
  styleUrls: ['./ChangePassword.component.scss']
})
export class ChangePasswordComponent implements OnInit {
  public editForm: FormGroup;
  constructor(
    public fb: FormBuilder,
    public authService: AuthService,
    public router: Router,
    private validateService: ValidateService,
    public dialogRef: MatDialogRef<ChangePasswordComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {user: any}
  ) {
    this.editForm = this.fb.group({
      password: [''],
      new_password: [''],
      confirm_password: [''],
    });
  }

  ngOnInit() {
  }

  public submitData(): void {
      if(!this.validateService.validatePassword(this.editForm.value.new_password)) {
        this.editForm.controls['new_password'].setErrors({ 'incorrect': true });
        return;
      }
      if(this.editForm.value.new_password !== this.editForm.value.confirm_password) {
        this.editForm.controls['confirm_password'].setErrors({ 'incorrect': true });
        return;
      }

    this.authService.changePassword(this.data.user.id,this.editForm.value).subscribe(
      {
        next: () => {
          this.editForm.reset();
          this.dialogRef.close();
        },
        error: (error:any) => {
          this.handleError(error);
        }
      }
    );
  }

  public cancel() {
    this.dialogRef.close();
  }

  public handleError(error: HttpErrorResponse): any {
    if (error.status === 409) {
      this.editForm.controls['new_password'].setErrors({ 'conflict': true });
    }
  }
}
