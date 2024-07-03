import axios from 'axios'

export default {
  getAgents(params) {
    return axios.get('/agents', {
      params
    })
  },
  editAgent(id, payload) {
    return axios.patch(`/agents/${id}`, payload)
  },
  saveAgent(payload) {
    // console.log('services/api payload :', payload)
    return axios.post('/agents/', payload)
  },
  deleteAgent(id) {
    return axios.delete(`/agents/${id}`)
  }
}
