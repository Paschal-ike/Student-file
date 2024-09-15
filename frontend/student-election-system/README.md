## Overview

This frontend is built using **React.js**. It allows admin users to log in, upload student data files, and view the status of their uploads.

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Technologies Used

- **React.js**: Core framework
- **Axios**: To handle API requests
- **React Router**: For routing within the application
- **React Toastify**: For notifications
- **CSS**: For basic styling

---

### Available Pages
### 1. Admin Login Page
URL: /login
Purpose: Allows admin users to log in by entering credentials.
### 2. Dashboard
URL: /dashboard
Purpose: Allows admin users to upload files and manage student data.
### 3. Uploads Page
URL: /uploads
Purpose: Displays a list of all uploaded files along with their statuses.
Protected Routes
The routes like the dashboard and file uploads are protected, meaning that only authenticated users with a valid JWT token can access them.

### Axios and Token Management
Axios is configured to automatically include authentication tokens in all requests. Tokens are stored in localStorage.
If a token expires, the system will attempt to refresh it using the /refresh-token/ endpoint.