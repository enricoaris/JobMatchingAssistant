import { yellow } from "@mui/material/colors";

export const JobStatus = {
    // Initial states
    UPLOADED: 0,
    QUEUED: 1,
    
    // Processing states
    GENERATING_EMBEDDING: 10,
    EXTRACTING_SKILLS: 11,
    EXTRACTING_REQUIREMENTS: 12,
    EXTRACTING_HIGHLIGHTS: 13,
    
    // Terminal states
    COMPLETED: 20,
    FAILED: 30,
    
    // Mock states
    MOCK_PROCESSING: 40,
    MOCK_COMPLETED: 41,
} as const;

export type JobStatus = typeof JobStatus[keyof typeof JobStatus];

// Job Status Config
export const JobStatusConfig: Record<JobStatus, {
    display: string;
    progress: number;
    color: 'gray' | 'blue' | 'yellow' | 'green' | 'red' | 'purple';
}> = {
    [JobStatus.UPLOADED]: { 
        display: 'Uploaded', 
        progress: 0, 
        color: 'gray',
         
    },
    [JobStatus.QUEUED]: { 
        display: 'Queued', 
        progress: 5, 
        color: 'blue',
         
    },
    [JobStatus.GENERATING_EMBEDDING]: { 
        display: 'Generating Embedding', 
        progress: 25, 
        color: 'yellow',
         
    },
    [JobStatus.EXTRACTING_SKILLS]: { 
        display: 'Extracting Skills', 
        progress: 50, 
        color: 'yellow',
         
    },
    [JobStatus.EXTRACTING_REQUIREMENTS]: { 
        display: 'Extracting Requirements', 
        progress: 75, 
        color: 'yellow',
         
    },
    [JobStatus.EXTRACTING_HIGHLIGHTS]: { 
        display: 'Extracting Highlights', 
        progress: 90, 
        color: 'yellow',
         
    },
    [JobStatus.COMPLETED]: { 
        display: 'Completed', 
        progress: 100, 
        color: 'green',
         
    },
    [JobStatus.FAILED]: { 
        display: 'Failed', 
        progress: 0, 
        color: 'red',
         
    },
    [JobStatus.MOCK_PROCESSING]: { 
        display: 'Mock Processing', 
        progress: 50, 
        color: 'purple',
         
    },
    [JobStatus.MOCK_COMPLETED]: { 
        display: 'Mock Complete', 
        progress: 100, 
        color: 'green',
         
    },
};

export const ResumeStatus = {
    // Initial states
    UPLOADED: 0,
    QUEUED: 1,
    
    // Processing states
    TEXT_EXTRACTED: 10,

    GENERATING_EMBEDDING: 20,
    EXTRACTING_SKILLS: 21,
    EXTRACTING_REQUIREMENTS: 22,
    EXTRACTING_HIGHLIGHTS: 23,
    
    // Matching states
    MATCHING: 30,
    MATCHING_COMPLETE: 31,
    
    // Terminal states
    COMPLETED: 40,
    FAILED: 50,
    
    // Mock states
    MOCK_PROCESSING: 60,
    MOCK_COMPLETED: 61,
} as const;

export type ResumeStatus = typeof ResumeStatus[keyof typeof ResumeStatus];

export const ResumeStatusConfig: Record<ResumeStatus, {
    display: string;
    progress: number;
    color: 'gray' | 'blue' | 'yellow' | 'green' | 'red' | 'purple';
     
}> = {
    [ResumeStatus.UPLOADED]: { 
        display: 'Uploaded', 
        progress: 0, 
        color: 'gray',
         
    },
    [ResumeStatus.QUEUED]: { 
        display: 'Queued', 
        progress: 5, 
        color: 'blue',
         
    },
    [ResumeStatus.TEXT_EXTRACTED]: {
        display: 'Text Extracted',
        progress: 15,
        color: 'yellow'
    },
    [ResumeStatus.GENERATING_EMBEDDING]: { 
        display: 'Generating Embedding', 
        progress: 20, 
        color: 'yellow',
         
    },
    [ResumeStatus.EXTRACTING_SKILLS]: { 
        display: 'Extracting Skills', 
        progress: 40, 
        color: 'yellow',
         
    },
    [ResumeStatus.EXTRACTING_REQUIREMENTS]: { 
        display: 'Extracting Requirements', 
        progress: 60, 
        color: 'yellow',
         
    },
    [ResumeStatus.EXTRACTING_HIGHLIGHTS]: { 
        display: 'Extracting Highlights', 
        progress: 70, 
        color: 'yellow',
         
    },
    [ResumeStatus.MATCHING]: { 
        display: 'Matching Jobs', 
        progress: 90, 
        color: 'blue',
         
    },
    [ResumeStatus.MATCHING_COMPLETE]: { 
        display: 'Matching Complete', 
        progress: 95, 
        color: 'green',
         
    },
    [ResumeStatus.COMPLETED]: { 
        display: 'Completed', 
        progress: 100, 
        color: 'green',
         
    },
    [ResumeStatus.FAILED]: { 
        display: 'Failed', 
        progress: 0, 
        color: 'red',
         
    },
    [ResumeStatus.MOCK_PROCESSING]: { 
        display: 'Mock Processing', 
        progress: 50, 
        color: 'purple',
         
    },
    [ResumeStatus.MOCK_COMPLETED]: { 
        display: 'Mock Complete', 
        progress: 100, 
        color: 'green',
         
    },
};

// ==================== Types ====================

export type DocumentType = 'job' | 'resume';

// ==================== Helper Functions ====================

export function getStatusConfig(documentType: DocumentType, status: number | string | null | undefined) {
    if (status === null || status === undefined) {
        return documentType === 'job' 
            ? JobStatusConfig[JobStatus.UPLOADED]
            : ResumeStatusConfig[ResumeStatus.UPLOADED];
    }

    // Handle string status
    if (typeof status === 'string') {
        // Try to parse as number
        const numValue = parseInt(status);
        if (!isNaN(numValue)) {
            return getStatusConfig(documentType, numValue);
        }
        
        // Try to find by enum name
        if (documentType === 'job') {
            const key = status as keyof typeof JobStatus;
            if (key in JobStatus) {
                return JobStatusConfig[JobStatus[key]];
            }
        } else {
            const key = status as keyof typeof ResumeStatus;
            if (key in ResumeStatus) {
                return ResumeStatusConfig[ResumeStatus[key]];
            }
        }
        
        // Try to find by display name
        const configs = documentType === 'job' ? JobStatusConfig : ResumeStatusConfig;
        for (const config of Object.values(configs)) {
            if (config.display === status) {
                return config;
            }
        }
        
        return null;
    }

    // Handle number status
    if (documentType === 'job') {
        if (status in JobStatusConfig) {
            return JobStatusConfig[status as JobStatus];
        }
        return JobStatusConfig[JobStatus.UPLOADED];
    } else {
        if (status in ResumeStatusConfig) {
            return ResumeStatusConfig[status as ResumeStatus];
        }
        return ResumeStatusConfig[ResumeStatus.UPLOADED];
    }
}

export function isStatusProcessing(documentType: DocumentType, status: number | string | null | undefined): boolean {
    if (status === null || status === undefined) return false;
    
    const numStatus = typeof status === 'string' ? parseInt(status) : status;
    if (isNaN(numStatus)) return false;
    
    if (documentType === 'job') {
        return numStatus === JobStatus.QUEUED ||
            numStatus === JobStatus.UPLOADED ||
            numStatus === JobStatus.GENERATING_EMBEDDING ||
            numStatus === JobStatus.EXTRACTING_SKILLS ||
            numStatus === JobStatus.EXTRACTING_REQUIREMENTS ||
            numStatus === JobStatus.EXTRACTING_HIGHLIGHTS ||
            numStatus === JobStatus.MOCK_PROCESSING;
    } else {
        return numStatus === ResumeStatus.QUEUED ||
            numStatus === ResumeStatus.UPLOADED ||
            numStatus === ResumeStatus.GENERATING_EMBEDDING ||
            numStatus === ResumeStatus.EXTRACTING_SKILLS ||
            numStatus === ResumeStatus.EXTRACTING_REQUIREMENTS ||
            numStatus === ResumeStatus.EXTRACTING_HIGHLIGHTS ||
            numStatus === ResumeStatus.MATCHING ||
            numStatus === ResumeStatus.MATCHING_COMPLETE ||
            numStatus === ResumeStatus.MOCK_PROCESSING;
    }
}

export function isStatusTerminal(documentType: DocumentType, status: number | string | null | undefined): boolean {
    if (status === null || status === undefined) return false;
    
    const numStatus = typeof status === 'string' ? parseInt(status) : status;
    if (isNaN(numStatus)) return false;
    
    if (documentType === 'job') {
        return numStatus === JobStatus.COMPLETED ||
               numStatus === JobStatus.FAILED ||
               numStatus === JobStatus.MOCK_COMPLETED;
    } else {
        return numStatus === ResumeStatus.COMPLETED ||
               numStatus === ResumeStatus.FAILED ||
               numStatus === ResumeStatus.MOCK_COMPLETED;
    }
}

export function getStatusProgress(documentType: DocumentType, status: number | string | null | undefined): number {
    const config = getStatusConfig(documentType, status);
    return config?.progress ?? 0;
}

export function getStatusDisplay(documentType: DocumentType, status: number | string | null | undefined): string {
    console.log(documentType)
    console.log(status)

    const config = getStatusConfig(documentType, status);
    return config?.display ?? 'Unknown';
}