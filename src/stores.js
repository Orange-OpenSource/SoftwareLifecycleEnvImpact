import { writable } from 'svelte-local-storage-store';

const user = 'test@test.fr'
const pass = 'test'

export const store = writable(null);

let sessions = []

export const getUserDetails = async(username, password) => {
    if (username === user && password === pass)
        return 1
}