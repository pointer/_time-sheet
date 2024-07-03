import axios from 'axios'

export default {
  getAllEquipments() {
    return axios.get('/equipment/all')
  }
}
