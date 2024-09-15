import React, { useState, useEffect } from 'react';
import axios from '../utils/axiosInstance';
import { toast } from 'react-toastify';
import './UploadsList.css';

const UploadsList = () => {
  const [uploads, setUploads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUploads = async () => {
      try {
        const response = await axios.get('/uploads/');
        setUploads(response.data);
      } catch (error) {
        console.error('Error fetching uploads:', error);
        setError('Failed to load uploads.');
        toast.error('Failed to load uploads.');
      } finally {
        setLoading(false);
      }
    };

    fetchUploads();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="uploads-container">
      <h2>Uploaded Files</h2>
      <table className="uploads-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>File Name</th>
            <th>Status</th>
            <th>Created At</th>
            <th>Updated At</th>
          </tr>
        </thead>
        <tbody>
          {uploads.map((upload) => (
            <tr key={upload.id}>
              <td>{upload.id}</td>
              <td>{upload.file_name}</td>
              <td>{upload.status}</td>
              <td>{new Date(upload.created_at).toLocaleString()}</td>
              <td>{new Date(upload.updated_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UploadsList;
