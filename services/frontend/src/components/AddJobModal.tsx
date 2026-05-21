import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField
} from "@mui/material";
import { useState, type Dispatch, type SetStateAction } from "react";
import { ApiService } from "../services/ApiService";
import type JobRow from "./JobGrid";
import Swal from 'sweetalert2';

interface JobModalProps {
  isOpen: boolean;
  onClose: () => void;
  sessionId: string | null;
  updateJobRow: Dispatch<SetStateAction<JobRow[]>>
}

const AddJobModal: React.FC<JobModalProps> = ({ isOpen, onClose, sessionId, updateJobRow }) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const uploadSingleJob = async () => {
    if (name === "" || description === ""){
      return false;
    }

    Swal.fire({
      title: 'Uploading Job...',
      didOpen: () => {
        Swal.showLoading();
      },
      allowOutsideClick: false
    });

    try {
      const response = await fetch(ApiService.job.upload, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          title: name,
          description: description,
          sessionId: sessionId
        })
      });

      if (response.status == 200){
        Swal.fire('Success!', 'Job is being processed.', 'success');

        const data = await response.json();
        const jobRow: JobRow = {
            id: data,
            status: "processing",
            title: name
          }

        updateJobRow(prev => [
          ...prev,
          jobRow
        ])

        return true;
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';
      Swal.fire('Error', errorMessage, 'error');
      console.error("Upload failed", error)
    }
  }

  const handleSubmit = async () => {
    var res = await uploadSingleJob();
    if (res){
      setName("");
      setDescription("");
      onClose();
    }
  };

  return (
    <Dialog open={isOpen} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Create Job</DialogTitle>

      <DialogContent>
        <TextField
          fullWidth
          label="Job Title"
          margin="normal"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <TextField
          fullWidth
          label="Description"
          margin="normal"
          multiline
          rows={3}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button variant="contained" onClick={handleSubmit}>
          Submit
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AddJobModal;