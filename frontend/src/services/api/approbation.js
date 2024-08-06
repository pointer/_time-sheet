import axios from 'axios'

const baseUrl = import.meta.env.VITE_SRV_API_URL;

export default {
  getApprobations(params) {
    const token = localStorage.getItem('token')?.replace(/"/g, '');
    return axios.get(`${baseUrl}/api/approbations`,params, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  }).catch(error => {
    console.error('Error in Get Approbations:', error.response ? error.response.data : error);
    throw error;
  });
  },
  editApprobation(id, payload) {
    return axios.patch(`${baseUrl}/approbation/${id}`, payload)
  },

saveApprobation(payload) {
    console.log(payload)
    return axios.post(`${import.meta.env.VITE_SRV_API_URL}/api/approbation`, payload, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  }).catch(error => {
    console.error('Error in saveApprobation:', error.response ? error.response.data : error);
    throw error;
  });
 },
  deleteApprobation(id) {
    return axios.delete(`${baseUrl}/approbation/${id}`)
  }
}