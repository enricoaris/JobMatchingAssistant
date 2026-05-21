
import AddIcon from '@mui/icons-material/Add';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import React, { useContext, useEffect, useMemo, useState } from "react";
import { Button, Box, Typography, Stack, Paper } from '@mui/material';
import { useDropzone } from 'react-dropzone';
import * as Papa from "papaparse"
import AddJobModal from '../components/AddJobModal';
import Navbar from '../components/Navbar';
import { ApiService } from '../services/ApiService';
import { JobGrid } from '../components/JobGrid';
import type JobRow from '../components/JobGrid';
import { SignalRContext } from '../components/SignalRProvider';
import Swal from 'sweetalert2';

interface ApiJob {
  id: string;
  name: string;
  status: string;
  vector: Boolean;
}

interface JobDataApiResponse{
   jobs: ApiJob[]
}

const UploadJob: React.FC = () => {
   const REQUIRED_COLUMNS = ['Title', 'Description'];
   const [file, setFile] = useState<File | null>();
   const [isModalOpen, setIsModalOpen] = useState(false);
   const [jobRows, setJobRows] = useState<JobRow[]>([]);

   const context = useContext(SignalRContext);
   
   if (!context) return <div>Loading connection...</div>;

   const { sessionId, signalRState } = context;

   const mergedJobRows = useMemo(() => {
      const statusMap = new Map(
         signalRState.jobStatus.map((item) => [item.id, item.status])
      )

      return jobRows.map(job => ({
         ...job,
         status: statusMap.get(job.id) ?? job.status
      }));
   }, [jobRows, signalRState.jobStatus]);
 
   const {getRootProps, getInputProps} = useDropzone({
      accept: {
         'text/csv': ['.csv'],
         'application/vnd.ms-excel': ['.csv']
      },
      multiple: false,
      onDrop: (acceptedFiles) => {
         const acceptedFile = acceptedFiles[0]

         Papa.parse(acceptedFile, {
            header: true,
            preview: 1,
            complete: (results) => {
               const fileHeaders = results.meta.fields;

               const isValid = REQUIRED_COLUMNS.every(col => fileHeaders?.includes(col));

               if (isValid){
                  setFile(acceptedFile);
               } else {
                  alert(`INvalid format. Please ensure columns are: ${REQUIRED_COLUMNS.join('. ')}`)
               }
            },
            error: (error) => {
               console.error("Error Parsing Csv:", error.message)
            }
         })
      }
   });

   useEffect(() => {
      var fetchJobData = async () => {
         var response = await fetch(ApiService.job.getJobs);
         var data = await response.json() as JobDataApiResponse;

         const jobRow: JobRow[] = data.jobs.map((job): JobRow => ({
            id: job.id,
            status: job.status,
            title: job.name
         }));

         setJobRows(jobRow)
      }
      
      fetchJobData();
   }, []);

   useEffect(() => {
      const uploadJobBatch = async () => {
         if (file != null){
            Swal.fire({
               title: 'Uploading Job...',
               didOpen: () => {
                  Swal.showLoading();
               },
               allowOutsideClick: false
            });

            const formData = new FormData();
            formData.append("file", file);

            try {
               const response = await fetch(ApiService.job.batchUpload, {
                  method: "POST",
                  body: formData
               });

               if (response.status == 200){
                  Swal.fire('Success!', 'Jobs are being processed.', 'success');

                  const data = await response.json() as JobDataApiResponse;

                  const addedJobs: JobRow[] = data.jobs.map((job): JobRow => ({
                     id: job.id,
                     title: job.name,
                     status: "Processing"
                  }));
                  
                  setJobRows(prev => [
                     ...prev,
                     ...addedJobs
                  ])

                  return true;
               }
            } catch (error) {
               const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';
               Swal.fire('Error', errorMessage, 'error');
               console.error("Upload failed", error)
            }  
         }
      }

      uploadJobBatch();

   }, [file])

   return (
      <Stack spacing={4} sx={{ padding: 4 }}>
         <Navbar/>

         <AddJobModal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            sessionId={sessionId}
            updateJobRow={setJobRows}
         />

         <Typography variant="h2">
               Job Management
         </Typography>
         
         <Paper 
            sx={{ 
               p: 3, 
               borderRadius: 2, 
               maxWidth: 1000, // Limits width so it doesn't stretch too far
               minWidth: 500,
               width: 750,
               bgcolor: 'background.paper' 
            }}
         >

         <Box sx={{ mb: 5 }}>
            <Typography variant="h6" component="h2" sx={{ fontWeight: 700, color: '#1a2027' }}>
               Upload Job
            </Typography>
            <Typography variant="body2" color="text.secondary">
               Import multiple listings or create a new job post manually.
            </Typography>
         </Box>

         <Stack 
            direction="row"
            spacing={2}
         >
            <Box {...getRootProps()} sx={{ flex: 1 }}>
               <input {...getInputProps()}/>
               <Button 
                  fullWidth
                  variant="outlined" 
                  startIcon={<UploadFileIcon />}
                  sx={{ textTransform: 'none', fontWeight: 600 }}
               >
                  Upload Jobs
               </Button>
            </Box>

            <Box sx={{ flex: 1 }}>
               <Button 
               fullWidth 
               variant="contained" 
               startIcon={<AddIcon />}
               sx={{ 
                  textTransform: 'none', 
                  fontWeight: 600,
                  boxShadow: 'none', // Flat look is very "modern SaaS"
                  '&:hover': { boxShadow: '0px 4px 10px rgba(0,0,0,0.1)' } 
               }}
               onClick={() => setIsModalOpen(true)}
            >
               Add A Job
            </Button>
            </Box>
         </Stack>

         <Stack>
            <JobGrid rows={mergedJobRows} setRows={setJobRows}/>
         </Stack>
      </Paper>
      </Stack>
   )
}
export default UploadJob