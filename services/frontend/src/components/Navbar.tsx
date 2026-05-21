import { AppBar, Box, Button, Toolbar, Typography } from "@mui/material"
import { useNavigate } from "react-router-dom";

const Navbar = () => {
    const navigate = useNavigate();
    return (
        <AppBar>
            <Toolbar>
                <Typography variant="h6">
                    Match Hub
                </Typography>

                <Box sx={{ flexGrow: 1 }} />

                <Box sx={{
                    display: "flex",
                    gap: 2,
                    justifyContent: "space-between",
                    maxWidth: 400 // optional: prevents too much stretching
                }}>
                    <Button color="inherit" onClick={() => navigate("/")}>Dashboard</Button>
                    <Button color="inherit" onClick={() => navigate("/job")}>Jobs</Button>
                    <Button color="inherit" onClick={() => navigate("/resume")}>Resume</Button>
                </Box>
            </Toolbar>

            
        </AppBar>
    )
}

export default Navbar;