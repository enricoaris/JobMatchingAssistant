import { IconButton } from "@mui/material";
import { DataGrid, type GridColDef } from "@mui/x-data-grid";
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { useNavigate } from "react-router-dom";
import { ApiService } from "../services/ApiService";
import Swal from "sweetalert2";

export default interface ResumeRow{
    id: string;
    title: string;
    status: any | null;
}

interface ResumeGridProps{
    rows: ResumeRow[];
    setRows: React.Dispatch<React.SetStateAction<ResumeRow[]>>
}

export const ResumeGrid: React.FC<ResumeGridProps> = ({rows, setRows}) => {
    const navigate = useNavigate();

    const handleViewResult = (matchId: string) => {
        navigate(`/matches/${matchId}`);
    }

    const handleDelete = async (id: string) => {
        try {
            Swal.fire({
                title: 'Deleting Resume...',
                didOpen: () => {
                Swal.showLoading();
                },
                allowOutsideClick: false
            });

            const response = await fetch(ApiService.resume.delete + `?id=${id}`, {
                method: "DELETE",
                headers: {
                    'Content-Type': 'application/json',
                },
            })

            if (response.ok){
                Swal.fire('Success!', 'Resume has been deleted.', 'success');
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

    const columns: GridColDef<ResumeRow>[] = [
        { field: "title", headerName: "Title", flex: 1 },
        {
            field: "status",
            headerName: "Status",
            flex: 1
        },
        {
            field: "actions",
            headerName: "Actions",
            type: "actions",
            flex: 1,
            renderCell: (params) => (
                <>
                    <IconButton
                        color="info"
                        onClick={() => handleViewResult(params.id.toString())}
                    >
                        <VisibilityIcon/>
                    </IconButton>
                    <IconButton
                        color="error"
                        onClick={() => handleDelete(params.id.toString())}
                    >
                        <DeleteIcon/>
                    </IconButton>
                </>
            ),
        },
    ]

    return (
        <div style={{ width: "100%" }}>
            <DataGrid
                rows={rows}
                columns={columns}
            />
        </div>
    );
}