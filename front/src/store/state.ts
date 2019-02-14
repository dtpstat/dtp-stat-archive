import { StateType } from '@/types';

function createState(): StateType {
    return {
        filters: null,
        mvcs: null
    }
}

export default createState