import React from 'react'
import { Box, Typography, Chip, LinearProgress, CircularProgress, Tooltip} from '@mui/material'
import {
    getStatusConfig,
    isStatusProcessing,
    isStatusTerminal
} from '../types/documentStatus'

import type { DocumentType } from '../types/documentStatus'

interface DocumentStatusBadgeProps {
    documentType: DocumentType;
    status: number | string | null | undefined;
    showProgress?: boolean;
    size?: 'small' | 'medium';
}

export const DocumentStatusBadge: React.FC<DocumentStatusBadgeProps> = ({
    documentType,
    status,
    showProgress = true,
    size = 'medium'
}) => {
    const config = getStatusConfig(documentType, status)

    if (!config) {
        return <Chip label="unknown" size={size} color='default'/>
    }

    const isProcessing = isStatusProcessing(documentType, status)
    const isTerminal = isStatusTerminal(documentType, status)
    const isFailed = documentType === 'job'
        ? status === 30
        : status === 40;
    
    const progressLessThan100 = config.progress > 0 && config.progress < 100;
    
    return (
        <Box sx={{display: 'flex', flexDirection: 'column', gap: 0.5, minWidth: 120}}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1}}>
                <Chip 
                    label={config.display}
                    size={size}
                    color={config.color as any}
                    variant={isFailed ? 'filled' : 'outlined'}
                    sx={{
                        fontWeight: 500,
                        ...(isProcessing && !isTerminal && {
                            animation: 'pulse 1.5s ease-in-out infinite',
                            '@keyframes pulse': {
                                 '0%': { opacity: 1 },
                                '50%': { opacity: 0.6 },
                                '100%': { opacity: 1 },
                            }
                        })
                    }}
                />

               

                {showProgress && (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    {isProcessing && progressLessThan100 ? (
                        // Indeterminate spinner for active processing
                        <CircularProgress size={20} thickness={4} color="primary" />
                    ) : (
                        <Tooltip title={`${config.progress}% complete`} placement='top'>
                            <LinearProgress
                                variant="determinate"
                                value={config.progress}
                                color={isFailed ? 'error' : 'primary'}
                                sx={{ 
                                    height: 4,
                                    borderRadius: 2,
                                    flex: 1,
                                    backgroundColor: 'action.hover',
                                    '& .MuiLinearProgress-bar': {
                                        borderRadius: 2,
                                    }
                                }}
                            />
                        </Tooltip>
                    )}
                </Box>
            )}

             {showProgress && config.progress > 0 && config.progress < 100 && (
                    <Typography variant='caption' color="text-secondary">
                        {config.progress}%
                    </Typography>
                )}
            </Box>

            {showProgress && (
                <Tooltip title={`${config.progress}% complete`} placement='top'>
                    <LinearProgress
                        variant="determinate"
                        value={config.progress}
                        color={isFailed ? 'error' : 'primary'}
                        sx={{ 
                            height: 4,
                            borderRadius: 2,
                            backgroundColor: 'action.hover',
                            '& .MuiLinearProgress-bar': {
                                borderRadius: 2,
                            }
                        }}
                    />
                </Tooltip>
            )} 
        </Box>
    )
}