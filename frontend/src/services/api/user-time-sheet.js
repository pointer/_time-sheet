import axios from 'axios'

const baseUrl = import.meta.env.VITE_SRV_API_URL;

export default {
  getTimesheets(params) {
    return axios.get(`${baseUrl}/timesheets`, { params })
  },
  editTimesheet(id, payload) {
    return axios.patch(`${baseUrl}/timesheet/${id}`, payload)
  },

saveTimesheet(payload) {
  console.log('Payload:', payload);
  const token = localStorage.getItem('token')?.replace(/"/g, '');
  return axios.post(`${baseUrl}/api/timesheet`, payload, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  }).catch(error => {
    console.error('Error in saveTimesheet:', error.response ? error.response.data : error);
    throw error;
  });
},
  deleteTimesheet(id) {
    return axios.delete(`${baseUrl}/timesheet/${id}`)
  }
}