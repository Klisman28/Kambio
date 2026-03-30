import Mock from "../mock";
import reviews from "./reviews";
import products from "./products";
import { categories, colors, sizes } from "./product-attributes";

Mock.onGet("/api/products").reply(({ params }) => {
  if (params && params.id) {
    const product = products.find((product) => product.id === +params.id);
    if (!product) return [200, false];
    return [200, product];
  }

  const limit = 10;
  const page = params?.page ? +params.page : 1;
  const offset = (page - 1) * limit;

  let filteredProducts = [...products];

  // PRODUCT FILTER BY SEARCH
  if (params && params.search) {
    filteredProducts = filteredProducts.filter((product) => {
      return (
        product.title.toLowerCase().includes(params.search.toLowerCase()) ||
        product.category.toLowerCase().includes(params.search.toLowerCase())
      );
    });
  }

  // PRODUCT FILTER BY STATUS
  if (params && params.status) {
    filteredProducts = filteredProducts.filter(
      (product) => product.status.toLowerCase() === params.status
    );
  }

  const total = filteredProducts.length;
  const totalPages = Math.ceil(total / limit);
  const lastOffset = offset + limit;

  const data = filteredProducts
    .sort((a, b) => (new Date(a.createdAt) > new Date(b.createdAt) ? -1 : 1))
    .slice(offset, lastOffset);

  const meta = {
    page,
    total,
    totalPages,
    firstIndex: offset,
    lastIndex: total > lastOffset ? lastOffset : total
  };

  return [200, { products: data, meta }];
});

Mock.onGet("/api/reviews").reply(({ params }) => {
  if (params && params.id) {
    return [200, reviews];
  }

  return [200, reviews];
});

Mock.onPost("/api/products").reply(({ data }) => {
  if (!data) return [400, { message: "Invalid request" }];

  const product = JSON.parse(data);
  products.push(product);
  return [200, { product }];
});

Mock.onPut("/api/products").reply(({ params, data }) => {
  if (!params || !data) return [400, { message: "Invalid request" }];

  const body = JSON.parse(data);
  const index = products.findIndex((product) => product.id === body.id);
  products[index] = body;
  return [200, { product: products[index] }];
});

Mock.onDelete("/api/products").reply(({ params }) => {
  if (!params.id) return [400, { message: "Invalid request" }];

  const index = products.findIndex((product) => product.id === +params.id);
  if (index < 0) return [404, { message: "User not found" }];
  const product = products[index];
  products.splice(index, 1);
  return [200, { product }];
});

// PRODUCT ATTRIBUTES
Mock.onGet("/api/products/categories").reply(() => {
  return [200, categories];
});

Mock.onGet("/api/products/colors").reply(() => {
  return [200, colors];
});

Mock.onGet("/api/products/sizes").reply(() => {
  return [200, sizes];
});
