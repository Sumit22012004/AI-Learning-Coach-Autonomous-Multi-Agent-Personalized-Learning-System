import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface AgentRequest {
    user_id: string;
    message: string;
    context?: Record<string, any>;
}

export interface AgentResponse {
    response: string;
    next_agent: string | null;
    current_state: Record<string, any>;
}

export const agentApi = {
    interact: async (payload: AgentRequest): Promise<AgentResponse> => {
        const response = await api.post<AgentResponse>('/agents/interact', payload);
        return response.data;
    },

    // Future endpoints
    // getCurriculum: ...
    // submitTask: ...
};

export default api;
