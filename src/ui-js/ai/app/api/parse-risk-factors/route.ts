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
Your job is to extract all of the risk factors from the following message as a list of json objects: {outputMessage}.
You should give specfic numbers for the min and max cost of each risk factor.
The format of the json objects should be:
[
    {{
        "title": "title of risk factor",
        "minCost": "min cost of risk factor (int)",
        "maxCost": "max cost of risk factor (int)",
        "description": "description of risk factor",
        "likelihood": "probability of risk factor (string)",
        "impact": "impact of risk factor (string)"
    }},
]
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
