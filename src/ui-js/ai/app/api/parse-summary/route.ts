import {
  ChatCompletionRequestMessage,
  Configuration,
  OpenAIApi,
} from "openai-edge";
import { OpenAIStream, StreamingTextResponse } from "ai";

// Create an OpenAI API client (that's edge friendly!)
const config = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(config);

// IMPORTANT! Set the runtime to edge
export const runtime = "edge";

var initialPrompt = `
Your job is to generate a summary for the following project: {outputMessage}.
Your summary should be formatted as follows:
{{
  "overview": "overview of project",
  "maxCost": "max cost predicted cost of project (float)",
  "minCost": "min cost predicted cost of project (float)",
  "expectedCost": "expected cost predicted cost of project (float)",
  "timeframe": "timeframe of project (months)",
  "impact": "impact of project (string)",
}}
ensure the answer is a valid JSON object parsable using JSON.parse(answer) return nothing else
`;

export async function POST(req: Request) {
  // Extract the `messages` from the body of the request
  var { messageContents } = await req.json();

  const messages = [
    {
      role: "user",
      content: initialPrompt.replace("{outputMessage}", messageContents),
    } as ChatCompletionRequestMessage,
  ];
  console.log(messages)
  // Ask OpenAI for a streaming chat completion given the prompt
  const response = await openai.createChatCompletion({
    model: "gpt-3.5-turbo-0613",
    stream: true,
    messages,
  });
  // Convert the response into a friendly text-stream
  const stream = OpenAIStream(response);
  // Respond with the stream
  return new StreamingTextResponse(stream);
}
