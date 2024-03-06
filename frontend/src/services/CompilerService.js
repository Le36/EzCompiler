import axios from 'axios'
import {useCompilerStore} from '@/stores/compilerStore'

const API_URL = 'http://localhost:5000'

export default {
    async submitCode(code) {
        try {
            const response = await axios.post(`${API_URL}/api/compile`, {code})
            const compilerStore = useCompilerStore()
            if (response.data.error) {
                compilerStore.setCompilationError(response.data.error)
            } else {
                compilerStore.setCompilationSuccess(response)
            }
            return response
        } catch (error) {
            console.error('Error submitting code:', error)
            throw error
        }
    }
}
