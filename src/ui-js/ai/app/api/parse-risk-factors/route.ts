
import { OpenAIStream, StreamingTextResponse } from 'ai';


export async function POST(req: Request) {
    const { prompt } = await req.json();

    // Ask OpenAI for a streaming completion given the prompt
    const response = await fetch('http://localhost:5000/parse_cost_drivers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    // Respond with the stream
    return new StreamingTextResponse(response);
}