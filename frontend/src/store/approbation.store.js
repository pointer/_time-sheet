import { defineStore } from 'pinia';
import { isPast, format, parseISO, addMinutes } from "date-fns";
import * as types from "@/store/mutation-types";
import router from "@/router";
import api from "@/services/api/approbation";
import timesheet_api from "@/services/api/user-time-sheet";
import { buildSuccess, handleError } from "@/utils/utils.js";


export const useApprobationStore = defineStore({
    id: 'approbation',
    state: () => ({
        approbation: null
    }),
    actions: {
        getApprobations({ month, token }) {
            return new Promise((resolve, reject) => {
                timesheet_api.getTimesheets(month, token)
                    .then((response) => {
                        if (response.status === 200) {
                            console.log(response.data);
                            this.approbation = response.data;
                            resolve(response.data);                            
                        } else {
                            reject(response.data);
                        }
                    })
                    .catch((error) => {
                        reject(error);
                    });
            });
        },
        editApprobation(id, payload) {
            return api.editApprobation(id, payload);
        },
        saveApprobation(payload) {
            return api.saveApprobation(payload);
        },
        deleteApprobation(id) {
            return api.deleteApprobation(id);
        },
        getTimesheetsByMonth(month, token) {
            return new Promise((resolve, reject) => {
                api.getTimesheetsByMonth(month, token)
                    .then((response) => {
                        if (response.status === 200) {
                            resolve(response.data);
                        } else {
                            reject(response.data);
                        }
                    })
                    .catch((error) => {
                        reject(error);
                    });
            });
        }
    }
});