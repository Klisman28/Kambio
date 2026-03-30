export interface Order {
  id: number;
  invoiceId: string;
  createAt: string;
  deliveredAt: string;
  customer: Customer;
  billing: string;
  shipping: string;
  status: string;
  payment: Payment;
  items: Item[];
  subTotalAmount: number;
  totalAmount: number;
  taxAmount: number;
  discountAmount: number;
  shippingChargeAmount: number;
}

export interface Item {
  id: number;
  name: string;
  image: string;
  price: number;
  quantity: number;
}

interface Customer {
  id: number;
  name: string;
  email: string;
  phone: string;
}

interface Payment {
  id: number;
  cardNumber: string;
  paymentMethod: string;
}
