import MockAdapter from "axios-mock-adapter";
import axios from "axios";

const Mock = new MockAdapter(axios, { delayResponse: 1000, onNoMatch: "throwException" });
export default Mock;
