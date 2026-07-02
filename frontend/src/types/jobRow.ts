import { JobStatus } from './documentStatus'

export default interface JobRow {
    id: string;
    title: string;
    status: JobStatus | number | string | null;
}