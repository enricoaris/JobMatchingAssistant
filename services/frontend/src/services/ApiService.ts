const API_URL = import.meta.env.VITE_API_BASE_URL

export const ApiService = {
    signalRUrl: API_URL + '/hubs/processing',
    createSession: API_URL + '/session',
    job: {
        upload: API_URL + '/job/upload',
        batchUpload: API_URL + '/job/batch-upload',
        stats: API_URL + '/job/stats',
        getJobs: API_URL + '/job',
        deleteJob: API_URL + '/job'
    },
    resume: {
        upload: API_URL + '/resume/upload',
        get_list: API_URL + '/resume',
        delete:  API_URL + '/resume/delete'
    },
    matchHub: {
        url: API_URL + '/matchHub'
    },
    match: {
        get_matches: API_URL + '/match'
    }
}