import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('Adding token to request:', `Bearer ${token}`);
    } else {
      console.log('No token found in localStorage.');
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => {
    // console.log('Response received:', response);
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({resolve, reject});
        }).then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token;
          return axiosInstance(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      return new Promise((resolve, reject) => {
        console.log('Attempting to refresh token...');
        axiosInstance.post('/refresh-token/', {
          refresh: localStorage.getItem('refreshToken')
        }).then((response) => {
          console.log('Refresh token response:', response);
          console.log('Response data:', response.data);
          console.log('Response status:', response.status);
          console.log('Response headers:', response.headers);

          if (response.data && response.data.access && response.data.refresh) {
            console.log('New access token:', response.data.access);
            console.log('New refresh token:', response.data.refresh);
            
            localStorage.setItem('token', response.data.access);
            localStorage.setItem('refreshToken', response.data.refresh);
            axiosInstance.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access;
            originalRequest.headers['Authorization'] = 'Bearer ' + response.data.access;
            
            console.log('Tokens updated in localStorage');
            processQueue(null, response.data.access);
            resolve(axiosInstance(originalRequest));
          } else {
            console.error('Unexpected response format from refresh token endpoint');
            processQueue(new Error('Refresh failed'), null);
            reject(new Error('Refresh failed'));
          }
        }).catch((refreshError) => {
          console.error('Error during token refresh:', refreshError);
          console.error('Error response:', refreshError.response);
          processQueue(refreshError, null);
          reject(refreshError);
        }).finally(() => {
          isRefreshing = false;
        });
      });
    }

    if (error.response) {
      console.error('Error response data:', error.response.data);
      console.error('Error status:', error.response.status);
      console.error('Error headers:', error.response.headers);
    } else if (error.request) {
      console.error('Error request:', error.request);
    } else {
      console.error('Error message:', error.message);
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;