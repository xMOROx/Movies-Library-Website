import {Component, Inject, OnInit} from '@angular/core';
import {FormBuilder, FormGroup} from "@angular/forms";
import {AuthService} from "../../../../../authentication/services/auth.service";
import {Router} from "@angular/router";
import {ValidateService} from "../../../../../core/services/validate.service";
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {HttpErrorResponse} from "@angular/common/http";

@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.scss']
})
export class EditProfileComponent implements OnInit {

  public editForm: FormGroup;

  constructor(    public fb: FormBuilder,
                  public authService: AuthService,
                  public router: Router,
                  private validateService: ValidateService,
                  public dialogRef: MatDialogRef<EditProfileComponent>,
                  @Inject(MAT_DIALOG_DATA) public data: {user: any}) {
    this.editForm = this.fb.group({
      email: [this.data.user.email],
      first_name: [this.data.user.first_name],
      last_name: [this.data.user.last_name],
    });
  }

  ngOnInit() {

  }


  public submitData(): void {
    if (!this.validateService.validateEmail(this.editForm.value.email)) {
      this.editForm.controls['email'].setErrors({ 'incorrect': true });
      return;

    }
    this.authService.updateProfile(this.data.user.id,this.editForm.value).subscribe(
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
      this.editForm.controls['email'].setErrors({ 'conflict': true });
    }
  }
}
