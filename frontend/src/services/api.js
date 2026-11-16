import axios from 'axios';

// Base URL for our FastAPI backend
const API_URL = 'http://localhost:8000/api';

export const api = {
  // Customer Endpoints
  submitRequest: (formData) => axios.post(`${API_URL}/customer/requests`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getCustomerRequests: () => axios.get(`${API_URL}/customer/requests`),

  // Owner Endpoints
  getOwnerRequests: () => axios.get(`${API_URL}/owner/requests`),
  approveRequest: (id) => axios.post(`${API_URL}/owner/requests/${id}/approve`),
  rejectRequest: (id) => axios.post(`${API_URL}/owner/requests/${id}/reject`),
};