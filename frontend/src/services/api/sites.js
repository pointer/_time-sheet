import axios from 'axios'

export default {
  getAllSites() {
    return axios.get('/sites/all')
  }
}
