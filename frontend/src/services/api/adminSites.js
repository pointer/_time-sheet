import axios from 'axios'

export default {
  getSites(params) {
    return axios.get('/sites', {
      params
    })
  },
  editSite(id, payload) {
    return axios.patch(`/sites/${id}`, payload)
  },
  saveSite(payload) {
    // console.log(payload)
    return axios.post('/sites/', payload)
  },
  deleteSite(id) {
    return axios.delete(`/sites/${id}`)
  }
}
