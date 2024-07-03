import axios from 'axios'

export default {
  getAssignments(params) {
    return axios.get('/assignments', {
      params
    })
  },
  editAssignment(id, payload) {
    return axios.patch(`/assignments/${id}`, payload)
  },
  saveAssignment(payload) {
    console.log(payload)
    return axios.post('/assignments/', payload)
  },
  deleteAssignment(id) {
    return axios.delete(`/assignments/${id}`)
  }
}
