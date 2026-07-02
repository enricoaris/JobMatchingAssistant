import { useNavigate, useParams } from "react-router-dom";
import { ApiService } from "../services/ApiService";
import { useEffect, useState } from "react";
import {
  Card,
  Text,
  Badge,
  Button,
  Group,
  Stack,
  Progress,
  List,
} from "@mantine/core";
import { Typography } from "@mui/material";

interface MatchDetail{
    id: string;
    title: string;
    score: number;
    matchLevel: string;
    assessment: string;
    keyGaps: string[];
    suggestions: string[];
}

interface MatchCardProps{
    match: MatchDetail
}

const MatchCard = ({match} : MatchCardProps) => {
    const getMatchColor = (matchLevel: string) => {
        switch (matchLevel) {
            case "strong":
            return "green";

            case "moderate":
            return "yellow";

            case "weak":
            return "red";

            default:
            return "gray";
        }
    };
    return (
        <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Stack style={{textAlign: "left"}}>
                <Group>
                    <div>
                        <Text>
                            {match.title}
                        </Text>
                    </div>

                    <Badge>
                        {match.score.toFixed(2)}% Match
                    </Badge>

                    <Badge color={getMatchColor(match.matchLevel)}>
                        {match.matchLevel}
                    </Badge>
                </Group>

                <Progress value={match.score}/>

                <Text size="sm">{match.assessment}</Text>

                <div>
                    <Text fw={600} mb={6}>
                        Suggestions
                    </Text>

                    <List spacing="xs" size="sm">
                        {match.suggestions.map((suggestion, index) => (
                        <List.Item key={index}>
                            {suggestion}
                        </List.Item>
                        ))}
                    </List>
                </div>
            </Stack>
        </Card>
    );
}

const MatchDetail: React.FC = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [matches, setMatches] = useState<MatchDetail[]>([]);

    const fetchMatchdata = async () => {
        const response = await fetch(ApiService.match.get_matches + `?resumeId=${id}`, {
            method: "GET"
        });

        if (response.ok){
            return response.json()
        }
    }

    useEffect(() => {
        const loadData = async () => {
            try{
                var matchesData = await fetchMatchdata();
                var matchRows: MatchDetail[] = matchesData.matches.map((item: any) => ({
                    id: item.jobId,
                    title: item.jobTitle,
                    score: item.score * 100,
                    matchLevel: item.matchLevel,
                    assessment: item.assessment,
                    keyGaps: item.keyGaps,
                    suggestions: item.suggestions
                }))

                setMatches(matchRows);
            }
            catch (error){
                await fetchMatchdata();
            }
        }

        loadData();
    }, []);

    return (
        <Stack>
            <Typography>
                <h1>
                    Matching Result
                </h1>
                
            </Typography>

            {matches.map((match) => (
                <MatchCard
                    key={match.id}
                    match={match}
                />
            ))}

            <Button onClick={() => navigate(`/resume`)}>
                Back
            </Button>
        </Stack>
    )
}

export default MatchDetail;