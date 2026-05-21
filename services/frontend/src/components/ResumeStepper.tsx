import { useEffect, useState, useMemo } from "react";
import { Box } from "@mui/material";

interface ResumeRow{
    id: string,
    sessionId: string,
    status: string
}

interface ResumeStepperProps{
    resumeId: string | null;
    resumeStatus: ResumeRow[];
}

export const ResumeStepper: React.FC<ResumeStepperProps> = ({resumeId, resumeStatus}) => {
    const mergedLogs = useMemo(() => {
        if (!resumeId) return [];

        return resumeStatus
            .filter(item => item.id === resumeId)
            .map(item => item.status);
    }, [resumeId, resumeStatus]);

    return (
        <Box sx={{
            background: "#000",
            color: "#00ff00",
            fontFamily: "monospace",
            p: 2,
            height: 200,
            overflow: "auto"
        }}>
            {mergedLogs.length > 0 ? (
                mergedLogs.map((log, i) => <div key={i}>{`> ${log}`}</div>)
            ) : (
                <div>No logs found for this ID...</div>
            )}
        </Box>
    )
}