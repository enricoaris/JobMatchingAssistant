import React, { useContext, useEffect, useState } from "react";
import { useDropzone } from "react-dropzone"
import Swal from 'sweetalert2';
import Navbar from "../components/Navbar";
import { Paper, Stack, Typography } from "@mui/material";
import {ResumeStepper} from "../components/ResumeStepper";
import { ApiService } from "../services/ApiService";
import { SignalRContext } from "../components/SignalRProvider";
import { ResumeGrid } from "../components/ResumeGrid";
import type ResumeRow from "../components/ResumeGrid";

const UploadResume: React.FC = () => {
    const [resumeRow, setResumeRow] = useState<ResumeRow[]>([]);
    const [file, setFile] = useState<File | null>(null);
    const [currentId, setCurrentId] = useState<string | null>(null);
    const context = useContext(SignalRContext);

    if (!context) return <div>Loading connection...</div>;

    const { sessionId, signalRState } = context;

    useEffect(() => {
        const loadData = async () => {
            try{
                var resumeData = await fetchResumeData();
                var resumeRow: ResumeRow[] = resumeData.resume.map((item : any)=> ({
                    id: item.resumeId,
                    title: item.title,
                    status: item.status
                }));

                setResumeRow(resumeRow);
            } catch (error) {
                console.error("Failed to fetch:", error);
            }
        }
        
        loadData();
    }, []);

    const fetchResumeData = async () => {
        const response = await fetch(ApiService.resume.get_list, {
            method: "GET"
        });

        if (response.ok){
            return response.json()
        }
    }

    const onDrop = (acceptedFiles: File[]) => {
        const file = acceptedFiles[0]
        setFile(file);
    }

    const { getRootProps, getInputProps } = useDropzone({
        accept: {
        "application/pdf": []
        },
        multiple : false,
        onDrop
    })

    const handleUpload =  async () => {
        if (!file) return;

        Swal.fire({
            title: 'Uploading Resume...',
            didOpen: () => {
                Swal.showLoading();
            },
            allowOutsideClick: false
        });

        try{
            const formData = new FormData();
            formData.append("File", file);
            formData.append("SessionId", sessionId ?? "")

            const response = await fetch(ApiService.resume.upload, {
                method: "POST",
                body: formData
            });

            if (response.ok){
                var data = await response.json();
                setCurrentId(data);
                Swal.fire('Done!', 'Resume is being processed.', 'success');
            } else {
                Swal.fire('Error!', 'Something went wrong..', 'error');
            }
        }
        catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';
            Swal.fire('Error', errorMessage, 'error');
            console.error("Upload failed", error)
        }  
    }

    return (
        <Stack spacing={4} sx={{padding:4}}>
            <Navbar/>
            <Typography variant="h2">
                Resume Management
            </Typography>

            {
                resumeRow.length > 0
                ? <ResumeGrid rows={resumeRow} setRows={setResumeRow}/>
                : <></>
            }
            

            <Stack spacing={3}>
                <Paper 
                    sx={{ 
                        p: 3, 
                        borderRadius: 2, 
                        maxWidth: 1000,
                        minWidth: 700,
                        bgcolor: 'background.paper',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: 3
                    }}
                >
                    <Typography variant="h5">
                        Upload Resume
                    </Typography>

                    {
                        file == null ? 
                            <div
                                {...getRootProps()}
                                style={{
                                    border: "2px dashed gray",
                                    padding: 40,
                                    textAlign: "center"
                                }}
                            >
                                <input {...getInputProps()} />
                                <p>Drag & drop resume here</p>
                            </div>
                            : <></>
                    }
                

                    {file && (
                        <p>Selected Files : {file.name}</p>
                    )}

                    <div>
                        <button onClick={handleUpload}>
                            Process Resume
                        </button>
                    </div>

                    {/* {
                        currentId !== null
                        ? <ResumeStepper resumeId={currentId} resumeStatus={signalRState.resumeStatus}/> 
                        : <></>
                    } */}
                </Paper>
            </Stack>
        </Stack>
    )
}

export default UploadResume;