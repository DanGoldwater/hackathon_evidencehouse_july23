import { Configuration, OpenAIApi } from "openai-edge";
import { OpenAIStream, StreamingTextResponse } from "ai";

// Create an OpenAI API client (that's edge friendly!)
const config = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(config);

// IMPORTANT! Set the runtime to edge
export const runtime = "edge";

var initialPrompt = `
The UK government is doing a procurement of {inputDescription}. 
Please give me a list of bullet points with key drivers of costs and key risks with this type of procurement
You should be extremely specific and detailed in your answers.
Return your answer in the format:

Overview:
...

Cost Drivers:
- Title: {title}
  Description: {description}
  MinCost (GBP): {minCost}
  MaxCost (GBP): {maxCost}

Risks:
- Title: {title}
  Description: {description}
  Likelihood: {likelihood}
  Impact: {impact}
  MinCost (GBP): {minCost}
  MaxCost (GBP): {maxCost}
...

Summary:
...
`;

var projectDescription = "";

export async function POST(req: Request) {
  // Extract the `messages` from the body of the request
  var { messages } = await req.json();

  if (messages.length === 1) {
    projectDescription = messages[0].content;
  }
  // Add first message as initial prompt
  initialPrompt.replace("{inputDescription}", projectDescription);
  messages.unshift({
    role: "user",
    content: initialPrompt,
  });

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




// async function runPythonScript(script: string): Promise<string[]> {
//   let options: object = {
//     mode: 'text',
//     pythonOptions: ['-u'], // get print results in real-time
//     scriptPath: 'path/to/your/python/script',
//     args: [script]
//   };

//   return new Promise((resolve, reject) => {
//     PythonShell.run('your_python_script.py', options).then(function (results) {
//       // results is an array consisting of messages collected during execution
//       console.log('results: %j', results);
//       resolve(results);
//     }).catch(function (err) {
//       console.log(err);
//       reject(err);
//     }
//     );
//   });
// }