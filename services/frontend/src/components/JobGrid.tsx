import * as React from "react";
import { DataGrid } from "@mui/x-data-grid";
import DeleteIcon from '@mui/icons-material/Delete';
import { IconButton } from '@mui/material';
import { type GridColDef } from '@mui/x-data-grid';
import Swal from 'sweetalert2';
import { ApiService } from "../services/ApiService";

export default interface JobRow{
    id: string;
    title: string;
    status: any | null;
}

interface JobGridProps{
    rows: JobRow[];
    setRows: React.Dispatch<React.SetStateAction<JobRow[]>>
}

export const JobGrid: React.FC<JobGridProps> = ({ rows, setRows }) => {
    const columns: GridColDef<JobRow>[] = [
        { field: "title", headerName: "Title", flex: 2 },
        {
            field: "status",
            headerName: "Status",
            width: 140,
            flex: 1
        },
        {
            field: "actions",
            headerName: "Actions",
            type: "actions",
            width: 100,
            renderCell: (params) => (
                <IconButton
                    color="error"
                    onClick={() => handleDelete(params.id.toString())}
                >
                    <DeleteIcon />
                </IconButton>
            ),
        },
    ];

    const handleDelete = async (id: string) => {
        try {
            Swal.fire({
                title: 'Deleting Job...',
                didOpen: () => {
                Swal.showLoading();
                },
                allowOutsideClick: false
            });

            const response = await fetch(`${ApiService.job.deleteJob}?id=${id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok){
                Swal.fire('Success!', 'Job has been deleted.', 'success');
                setRows((prev) => prev.filter((row) => row.id !== id));
            } else {
                Swal.fire('Failed!', 'Delete Failed.', 'error');
            }
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';
            Swal.fire('Error', errorMessage, 'error');
            console.error("Upload failed", error)
        }
    }

    return (
        <div style={{ height: 500, width: "100%" }}>
        <DataGrid
            rows={rows}
            columns={columns}
        />
        </div>
    );
}