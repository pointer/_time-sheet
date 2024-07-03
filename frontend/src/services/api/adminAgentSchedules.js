import axios from 'axios'

export default {
  getAgentSchedules(params) {
    return axios.get('/agentschedule', {
      params
    })
  },
  editAgentschedule(id, payload) {
    return axios.patch(`/agentschedule/${id}`, payload)
  },
  saveAgentschedule(payload) {
    console.log(payload)
    return axios.post('/agentschedule/', payload)
  },
  deleteAgentschedule(id) {
    return axios.delete(`/agentschedule/${id}`)
  }
}
