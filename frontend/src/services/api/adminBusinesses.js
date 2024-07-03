import axios from 'axios'

export default {
  getBusinesses(params) {
    return axios.get('/businesses', {
      params
    })
  },
  editBusiness(id, payload) {
    return axios.patch(`/businesses/${id}`, payload)
  },
  saveBusiness(payload) {
    return axios.post('/businesses/', payload)
  },
  deleteBusiness(id) {
    return axios.delete(`/businesses/${id}`)
  }
}
