import { HubConnection } from "@microsoft/signalr";
import { useEffect, useRef, useState, createContext, type ReactNode } from "react";
import { ApiService } from "../services/ApiService";
import * as signalR from "@microsoft/signalr";
import { JobStatus } from "../types/documentStatus";

interface SignalRState {
    resumeStatus: any[];
    jobStatus: Array<{
        id: string;
        status: JobStatus | number;
    }>;
}

interface SignalRContextType {
    connection: signalR.HubConnection | null;
    sessionId: string | null;
    signalRState: SignalRState
}

export const SignalRContext = createContext<SignalRContextType | undefined>(undefined);

export const SignalRProvider = ({ children }: {children: ReactNode}) => {
    const [signalRState, setSignalRState] = useState<SignalRState>({
        resumeStatus: [],
        jobStatus: []
    });

    const [connection, setConnection] = useState<HubConnection | null>(null);
    const [sessionId, setSessionId] = useState<string| null>(null);

    const isInitializing = useRef(false);

    useEffect(() => {
        if (isInitializing.current) return;
        isInitializing.current = true;

        const abortController = new AbortController();
        let hubConn: signalR.HubConnection | null = null;

        const setupConnection = async () => {
            try{
                let currentSession = localStorage.getItem("signalr_session_id");
                if (!currentSession) {
                    const response = await fetch(ApiService.createSession, {
                        method: "POST",
                        signal: abortController.signal
                    });

                    const {sessionId} =  await response.json();

                    if (abortController.signal.aborted) return;

                    currentSession = sessionId;
                    localStorage.setItem("signalr_session_id", currentSession!);
                }

                setSessionId(currentSession);

                hubConn = new signalR.HubConnectionBuilder()
                    .withUrl(ApiService.signalRUrl)
                    .withAutomaticReconnect()
                    .build()

                hubConn.on("jobStatusUpdate", (update: {id: string; status: number }) => {
                    setSignalRState(prev => ({
                        ...prev,
                        jobStatus: [...prev.jobStatus, update]
                    }));
                })

                hubConn.on("resumeStatusUpdate", (update: {id: string; status: number }) => {
                    console.log("status update")
                    console.log(update)
                    setSignalRState(prev => ({
                        ...prev,
                        resumeStatus: [...prev.resumeStatus, update]
                    }))
                })

                if (hubConn.state === "Disconnected"){
                    await hubConn.start();
                }
                
                await hubConn.invoke("JoinSession", currentSession);
                setConnection(hubConn)

                console.log("Connected to SignalR");
            } catch(error) {
                if (error === "AbortError") return;
                console.error("SignalR Setup Error:", error);
                
                return null;
            }
        }

        setupConnection();

        return () => {
            abortController.abort();
            isInitializing.current = false;
        }
    }, [])

    return (
        <SignalRContext.Provider value={{connection, sessionId, signalRState}}>
            {children}
        </SignalRContext.Provider>
    )
}