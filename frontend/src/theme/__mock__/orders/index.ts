import Mock from "../mock";
import { orderAnalytics, orderHistories, orders, paymentMethods, statuses } from "./orders";

Mock.onGet("/api/orders").reply(({ params }) => {
  if (params && params.id) {
    const order = orders.find((order) => order.id === params.id);
    if (!order) return [200, false];
    return [200, orders.find((order) => order.id === params.id)];
  }

  const limit = 10;
  const page = params?.page ? +params.page : 1;
  const offset = (page - 1) * limit;

  let filteredOrders = [...orders];

  // ORDERS FILTER BY SEARCH
  if (params && params.search) {
    const search = params.search.toLowerCase();
    filteredOrders = filteredOrders.filter((order) => {
      return (
        order.invoiceId.toLowerCase().includes(search) ||
        order.customer.name.toLowerCase().includes(search)
      );
    });
  }

  // FILTER BY STATUS
  if (params && params.status) {
    filteredOrders = filteredOrders.filter((order) => order.status.toLowerCase() === params.status);
  }

  // FILTER BY PAYMENT METHOD
  if (params && params.payment) {
    filteredOrders = filteredOrders.filter(
      (order) => order.payment.paymentMethod === params.payment
    );
  }

  const total = filteredOrders.length;
  const totalPages = Math.ceil(total / limit);
  const lastOffset = offset + limit;

  const data = filteredOrders
    .sort((a, b) => (new Date(a.createAt) > new Date(b.createAt) ? -1 : 1))
    .slice(offset, lastOffset);

  const meta = {
    page,
    total,
    totalPages,
    firstIndex: offset,
    lastIndex: total > lastOffset ? lastOffset : total
  };

  return [200, { orders: data, meta }];
});

Mock.onPatch("/api/orders").reply(({ params, data }) => {
  const index = orders.findIndex((order) => order.id === +params.id);
  if (index < 0) return [404, { message: "Order not found" }];
  orders[index] = { ...orders[index], ...data };
  return [200, { order: orders[index] }];
});

Mock.onGet("/api/orders/statues").reply(() => {
  return [200, statuses];
});

Mock.onGet("/api/orders/payment-methods").reply(() => {
  return [200, paymentMethods];
});

Mock.onGet("/api/orders/histories").reply(() => {
  return [200, orderHistories];
});

Mock.onGet("/api/orders/analytics").reply(() => {
  return [200, orderAnalytics];
});
