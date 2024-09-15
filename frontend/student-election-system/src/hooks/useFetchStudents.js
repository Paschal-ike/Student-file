// useFetchStudents.js
import { useState, useEffect } from 'react';
import axios from '../utils/axiosInstance';

const useFetchStudents = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await axios.get('/students/');
        setStudents(response.data);
      } catch (error) {
        console.error('Error fetching student data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStudents();
  }, []);

  return { students, loading };
};

export default useFetchStudents;
