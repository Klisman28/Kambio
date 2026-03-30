import Mock from "../mock";
import invoices from "./invoices";
import { users } from "../users/users";

Mock.onGet("/api/invoices").reply(({ params }) => {
  if (params && params.id) {
    return [200, invoices.find((invoice) => invoice.id === params.id)];
  }

  const limit = 10;
  const page = params?.page ? +params.page : 1;
  const offset = (page - 1) * limit;

  let filteredInvoices = [...invoices];

  // INVOICES FILTER BY SEARCH
  if (params && params.search) {
    const search = params.search.toLowerCase();
    filteredInvoices = filteredInvoices.filter((invoice) => {
      return (
        invoice.customer.name.toLowerCase().includes(search) ||
        invoice.billingAddress?.address.toLowerCase().includes(search) ||
        invoice.id.toString().toLowerCase().includes(search) ||
        invoice.dueDate.toString().toLowerCase().includes(search) ||
        invoice.totalAmount.toString().toLowerCase().includes(search)
      );
    });
  }

  // INVOICES FILTER BY STATUS
  if (params && params.status) {
    filteredInvoices = filteredInvoices.filter(
      (invoice) => invoice.status.toLowerCase() === params.status
    );
  }

  const total = filteredInvoices.length;
  const totalPages = Math.ceil(total / limit);
  const lastOffset = offset + limit;

  const data = filteredInvoices
    .sort((a, b) => (new Date(a.issueDate) > new Date(b.issueDate) ? -1 : 1))
    .slice(offset, lastOffset);

  const meta = {
    page,
    total,
    totalPages,
    firstIndex: offset,
    lastIndex: total > lastOffset ? lastOffset : total
  };

  return [200, { invoices: data, meta }];
});

Mock.onPost("/api/invoices").reply(({ data }) => {
  if (!data) return [400, { message: "Invalid request" }];

  const invoice = JSON.parse(data);

  invoice.id = invoices[invoices.length - 1].id + 1;
  const user = users[Math.floor(Math.random() * users.length)];
  invoice.customer = { id: user.id, name: user.name, image: user.image };

  invoices.push(invoice);
  return [200, { invoice }];
});

Mock.onPut("/api/invoices").reply(({ params, data }) => {
  if (!params || !data) return [400, { message: "Invalid request" }];

  const body = JSON.parse(data);
  const index = invoices.findIndex((invoice) => invoice.id === body.id);
  if (index < 0) return [404, { message: "Invoice not found" }];
  invoices[index] = body;
  return [200, { invoice: invoices[index] }];
});

Mock.onDelete("/api/invoices").reply(({ params }) => {
  if (!params.id) return [400, { message: "Invalid request" }];

  const index = invoices.findIndex((invoice) => invoice.id === params.id);
  if (index < 0) return [404, { message: "Invoice not found" }];
  invoices.splice(index, 1);
  return [200, { invoice: invoices[index] }];
});
