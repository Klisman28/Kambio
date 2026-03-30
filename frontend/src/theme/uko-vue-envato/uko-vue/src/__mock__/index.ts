import Mock from "./mock";

import "./users";
import "./orders";
import "./products";
import "./invoices";

Mock.onAny().passThrough();
