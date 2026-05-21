import { useState } from 'react';
import Navbar from '../components/Navbar';
import { Typography } from '@mui/material';

const Home: React.FC = () => {
    const [count, setCount] = useState(0);
    
    return (
        <>
            <Navbar/>
            <Typography>
                <h1>
                    Match Hub
                </h1>
            </Typography>
        </>
    )
}

export default Home;