import Mock from "../mock";
import { users, statues } from "./users";

Mock.onGet("/api/users").reply(({ params }) => {
  if (params && params.id) {
    return [200, users.find((user) => user.id === +params.id)];
  }

  const limit = 10;
  const page = params?.page ? +params.page : 1;
  const offset = (page - 1) * limit;

  let filteredUsers = [...users];

  // USER FILTER BY SEARCH
  if (params && params.search) {
    filteredUsers = filteredUsers.filter((user) => {
      return (
        user.name.toLowerCase().includes(params.search.toLowerCase()) ||
        user.email.toLowerCase().includes(params.search.toLowerCase()) ||
        user.address.toLowerCase().includes(params.search.toLowerCase()) ||
        user.phone.toLowerCase().includes(params.search.toLowerCase())
      );
    });
  }

  // USER FILTER BY STATUS
  if (params && params.status) {
    filteredUsers = filteredUsers.filter((user) => user.status.toLowerCase() === params.status);
  }

  const total = filteredUsers.length;
  const totalPages = Math.ceil(total / limit);
  const lastOffset = offset + limit;

  const data = filteredUsers
    .sort((a, b) => (new Date(a.createAt) > new Date(b.createAt) ? -1 : 1))
    .slice(offset, lastOffset);

  const meta = {
    page,
    total,
    totalPages,
    firstIndex: offset,
    lastIndex: total > lastOffset ? lastOffset : total
  };

  return [200, { users: data, meta }];
});

Mock.onPost("/api/users").reply(({ data }) => {
  if (!data) return [400, { message: "Invalid request" }];

  const user = JSON.parse(data);

  user.id = users[users.length - 1].id + 1;
  user.createAt = new Date().toDateString();
  user.image = "/images/users/14.jpg";

  users.push(user);
  return [200, { user }];
});

Mock.onPut("/api/users").reply(({ params, data }) => {
  if (!params || !data) return [400, { message: "Invalid request" }];

  const user = JSON.parse(data);
  const index = users.findIndex((u) => u.id === user.id);
  users[index] = user;
  return [200, { user }];
});

Mock.onDelete("/api/users").reply(({ params }) => {
  if (!params.id) return [400, { message: "Invalid request" }];

  const index = users.findIndex((user) => user.id === +params.id);
  if (index < 0) return [404, { message: "User not found" }];
  const user = users[index];
  users.splice(index, 1);
  return [200, { user }];
});

// USER STATUES
Mock.onGet("/api/users/status").reply(() => {
  return [200, statues];
});
