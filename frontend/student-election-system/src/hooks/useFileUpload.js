// useFileUpload.js
import { useState } from 'react';
import axios from '../utils/axiosInstance';
import { toast } from 'react-toastify';

const useFileUpload = () => {
  const [uploading, setUploading] = useState(false);

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploading(true);
      const response = await axios.post('/students/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      toast.success('File uploaded successfully!');
      return response.data;
    } catch (error) {
      toast.error('File upload failed.');
      throw error;
    } finally {
      setUploading(false);
    }
  };

  return { uploadFile, uploading };
};

export default useFileUpload;
