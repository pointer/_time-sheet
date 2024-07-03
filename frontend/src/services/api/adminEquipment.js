import axios from 'axios'

export default {
  getEquipments(params) {
    return axios.get('/equipment', {
      params
    })
  },
  editEquipment(id, payload) {
    return axios.patch(`/equipment/${id}`, payload)
  },
  saveEquipment(payload) {
    // console.log(payload)
    return axios.post('/equipment/', payload)
  },
  deleteEquipment(id) {
    return axios.delete(`/equipment/${id}`)
  }
}
