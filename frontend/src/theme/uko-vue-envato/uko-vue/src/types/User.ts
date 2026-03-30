export interface User {
  id: number;
  name: string;
  role: string;
  image: string;
  email: string;
  phone: string;
  status: string;
  address: string;
  createAt: string;
}

export interface UserPayload {
  name: string;
  role: string;
  image: string;
  email: string;
  phone: string;
  status: string;
  address: string;
}
