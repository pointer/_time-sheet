<template>
    <v-btn @click="handleLogout" color="error" dark>
        Logout
    </v-btn>
</template>

<script>
// import { userLogout } from '@/services/api/auth';
import router from '@/router'
export default {
    methods: {
        handleLogout() {
            localStorage.removeItem('token')
            localStorage.removeItem('tokenExpiration')
            localStorage.removeItem('user')
            // commit(types.LOGOUT)
            router.push({
                name: 'login'
            })
        }
    }
};
</script>