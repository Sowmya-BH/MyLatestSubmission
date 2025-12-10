//// src/api.js
// src/api.js
import axios from "axios";

// ----------------------------------------------------
// 1. AXIOS INSTANCE & CONFIG
// ----------------------------------------------------
const API = axios.create({
  baseURL: "http://localhost:8000",
});

// Attach token for each request (Interceptor ensures Authorization header is added)
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    //
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});


// ----------------------------------------------------
// 2. AUTH ENDPOINTS
// ----------------------------------------------------
// NOTE: registerUser is only used for initial setup by allowed users.
export const registerUser = (data) => API.post("/auth/register", data);
export const loginUser = (data) => API.post("/auth/login", data);


// ----------------------------------------------------
// 3. DOCUMENT MANAGEMENT ENDPOINTS
// ----------------------------------------------------
export const uploadPDF = (file) => {
  const formData = new FormData();
  formData.append("file", file); // Must match FastAPI parameter name: file
  return API.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const listDocs = () => API.get("/documents");

// Trigger analysis (runs crew in background)
export const analyzeDocument = (docId) => API.post(`/analyze/${docId}`);

// Get status and results (logs, summary)
export const getResults = (docId) => API.get(`/results/${docId}`);


// ----------------------------------------------------
// 4. DIRECT QUERY ENDPOINT
// ----------------------------------------------------
/**
 * Runs a query synchronously against a specific PDF.
 * @param {object} data - Payload containing query parameters.
 * @param {string} data.pdf_path - Absolute path to the PDF on the server.
 * @param {string} [data.input_field] - Optional keyword search term.
 * @param {string} [data.user_query] - Optional semantic query.
 */
export const queryPDF = (data) => {
  // Use the authorized 'API' instance and send JSON payload.
  return API.post("/query", data);
};

// ----------------------------------------------------
// 5. OLD/UNUSED FUNCTIONS (Removed for cleanliness)
// ----------------------------------------------------
//import axios from "axios";
//
//const API = axios.create({
//  baseURL: "http://localhost:8000",
//});
//
//// Attach token for each request
//API.interceptors.request.use((config) => {
//  const token = localStorage.getItem("token");
//  if (token) config.headers.Authorization = `Bearer ${token}`;
//  return config;
//});
//
//// AUTH
//export const registerUser = (data) => API.post("/auth/register", data);
//export const loginUser = (data) => API.post("/auth/login", data);
//
//// DOCUMENTS
//export const uploadPDF = (file) => {
//  const formData = new FormData();
//  formData.append("file", file);
//  return API.post("/upload", formData);
//};
//
//export const listDocs = () => API.get("/documents");
//
//// QUERY
//export async function queryPDF(question) {
//  try {
//    const response = await fetch(`${API_BASE_URL}/query`, {
//      method: "POST",
//      headers: { "Content-Type": "application/json" },
//      body: JSON.stringify({ question }),
//    });
//
//    if (!response.ok) {
//      throw new Error("Failed to query backend");
//    }
//
//    return await response.json();
//  } catch (error) {
//    console.error("Error querying PDF:", error);
//    throw error;
//  }
//}



//export const runQuery = (documentId, data) => {
//  return axios.post(`${API_URL}/query/${documentId}`, data, {
//    headers: {
//      Authorization: `Bearer ${localStorage.getItem("token")}`,
//    },
//  });
//};
//export const queryPDF = (docId, data) =>
//  API.post(`/query/${docId}`, data);



//import axios from "axios";
//
//const API = axios.create({
//  baseURL: "http://127.0.0.1:8000",
//});
//
//// Attach JWT token if present
//API.interceptors.request.use((config) => {
//  const token = localStorage.getItem("access_token");
//  if (token) {
//    config.headers.Authorization = `Bearer ${token}`;
//  }
//  return config;
//});
//
//// ---- Upload ONE PDF ----
//export const uploadPDF = async (file) => {
//  const formData = new FormData();
//  formData.append("file", file);   // MUST match FastAPI parameter name: file
//
//  return API.post("/upload", formData, {
//    headers: { "Content-Type": "multipart/form-data" },
//  });
//};
//
//// ---- List user documents ----
//export const listDocuments = async () => {
//  return API.get("/documents");
//};
//
//// ---- Trigger analysis ----
//export const analyzeDocument = async (id) => {
//  return API.post(`/analyze/${id}`);
//};
//
//// ---- Get analysis results ----
//export const getResults = async (id) => {
//  return API.get(`/results/${id}`);
//};
