export interface User {
  id?: number;
  email: String;
  password: String;
  first_name?: String;
  last_name?: String;
  roles?: Roles;
};

interface Roles {
  admin?: boolean;
  user?: boolean;
  staff?: boolean;
}
