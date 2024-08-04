import { defineStore } from "pinia";
import { isPast, format, parseISO, addMinutes } from "date-fns";
import * as types from '@/store/mutation-types'
import router from '@/router'
import api from '@/services/api/auth'
import { buildSuccess, handleError } from '@/utils/utils.js'
// import { fetchWrapper } from "@/helpers";
// import { router } from "@/router";
import { useAlertStore } from "@/store";

const MINUTES_TO_CHECK_FOR_TOKEN_REFRESH = 1440

// const baseUrl = `${import.meta.env.VITE_SRV_API_URL}`;

// async function localLogin(username, password) {
//   return new Promise((resolve, reject) => {
//     const ws = new WebSocket(baseUrl);
//     // const ws = new WebSocket("ws://localhost:8765");
//     ws.onopen = () => {
//       ws.send(JSON.stringify({ action: "login", username, password }));
//     };

//     ws.onmessage = (event) => {
//       const response = JSON.parse(event.data);
//       resolve(response);
//       ws.close();
//     };

//     ws.onerror = (error) => {
//       reject(error);
//     };
//   });
// }
export const useAuthStore = defineStore({
  id: "auth",
  state: () => ({
    user: JSON.parse(localStorage.getItem("user")),
    token: JSON.parse(localStorage.getItem('token')) || null,
    isTokenSet: !!localStorage.getItem('token'),
    returnUrl: null,
  }),

  // getters: {
  //   user: (state) => state.user,
  //   token: (state) => state.token,
  //   isTokenSet: (state) => state.isTokenSet
  // },

  actions: {
    userLogin(payload) {
      return new Promise((resolve, reject) => {
        // this.SHOW_LOADING(true);
        api
          .userLogin(payload)
          .then((response) => {
            if (response.status === 200) {
              localStorage.setItem('user', JSON.stringify(response.data.user));
              localStorage.setItem('token', JSON.stringify(response.data.access_token));
              localStorage.setItem('role', JSON.stringify(response.data.is_superuser));
              localStorage.setItem(
                'tokenExpiration',
                JSON.stringify(
                  format(
                    addMinutes(new Date(), MINUTES_TO_CHECK_FOR_TOKEN_REFRESH),
                    'X'
                  )
                )
              );
              this.user = response.data.user;
              this.token = response.data.token;
              this.isTokenSet = true;
              buildSuccess(
                null,
                this,
                resolve,
                router.push({ name: 'TimeSheet' })
                  .catch(error => {
                    console.error('Navigation failed:', error);
                    // Optionally, you can redirect to a default route or show an error message
                  })
              );
              console.log('Login successful');
            }
            else {
              const errorData = response.json();
              if (errorData.message === 'REGISTER_USER_ALREADY_EXISTS') {
                console.error('This email is already registered');
              // Handle this case in your UI, maybe show an error message to the user
              } else 
                console.error('Registration failed:', errorData.message);
              // Handle other types of errors
              } 
          })
      });
    },
    refreshToken({ commit }) {
      return new Promise((resolve, reject) => {
        api
          .refreshToken()
          .then((response) => {
            if (response.status === 200) {
              window.localStorage.setItem(
                'token',
                JSON.stringify(response.data.token)
              )
              window.localStorage.setItem(
                'tokenExpiration',
                JSON.stringify(
                  format(
                    addMinutes(new Date(), MINUTES_TO_CHECK_FOR_TOKEN_REFRESH),
                    'X'
                  )
                )
              )
              commit(types.SAVE_TOKEN, response.data.token)
              resolve()
            }
          })
          .catch((error) => {
            handleError(error, commit, reject)
          })
      })
    },
    autoLogin({ commit }) {
      const user = JSON.parse(localStorage.getItem('user'))
      commit(types.SAVE_USER, user)
      commit(types.SAVE_TOKEN, JSON.parse(localStorage.getItem('token')))
      commit(types.SET_LOCALE, JSON.parse(localStorage.getItem('locale')))
      commit(types.EMAIL_VERIFIED, user.verified)
    },
    userLogout({ commit }) {
      window.localStorage.removeItem('token')
      window.localStorage.removeItem('tokenExpiration')
      window.localStorage.removeItem('user')
      // commit(types.LOGOUT)
      router.push({
        name: 'login'
      })
    },
    userRegister(payload) {
      return new Promise((resolve, reject) => {
        api
          .userRegister(payload)
          .then((response) => {
            if (response.status === 200) {
              resolve(response);
            } else {
              reject(response);
            }
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
  },

  mutations: {
    [types.SAVE_TOKEN](state, token) {
      state.token = token;
      state.isTokenSet = true;
    },
    [types.LOGOUT](state) {
      state.user = null;
      state.token = null;
      state.isTokenSet = false;
    },
    [types.SAVE_USER](state, user) {
      state.user = user;
    }
  }
});