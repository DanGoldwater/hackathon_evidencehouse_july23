"use client";

import BasicTabs from "@/componenets/Tabs";
import { Message, useChat } from "ai/react";
import { useState } from "react";

export interface CostDriver {
  title: string;
  description: string;
  minCost: number;
  maxCost: number;
}

export interface RiskFactor {
  title: string;
  description: string;
  minCost: number;
  maxCost: number;
  likelihood: string;
  impact: string;
}

export interface SummaryStats {
  overview: string;
  maxCost: number;
  minCost: number;
  expectedCost: number;
  timeframe: number;
  impact: string;
  similairProjects: {
    name: string;
    expectedCost: number;
    actualCost: number;
    timeframe: number;
  }[];
}

export default function Chat() {
  const [summary, setSummary] = useState<SummaryStats>({} as SummaryStats);
  const [costDrivers, setCostDrivers] = useState<CostDriver[]>([]);
  const [riskFactors, setRiskFactors] = useState<RiskFactor[]>([]);

  async function onStreamComplete(outputMessage: Message) {
    // Get cost drivers
    if (costDrivers.length === 0 && riskFactors.length === 0) {
    //   const costDrivers = await fetch("/api/parse-cost-drivers", {
    //     method: "POST",
    //     body: JSON.stringify({
    //       messageContents: outputMessage.content,
    //     }),
    //   }).then(async (res) => {
    //     const reader = res.body?.getReader();
    //     const decoder = new TextDecoder("utf-8");
    //     let result = "";
    //     if (reader === undefined) {
    //       return;
    //     }
    //     // Read the stream
    //     while (true) {
    //       const { done, value } = await reader.read();

    //       if (done) {
    //         console.log(result);
    //         // The stream was fully read
    //         return JSON.parse(result) as CostDriver[];
    //       }

    //       // Decode the chunk and append it to the result
    //       result += decoder.decode(value);
    //     }
    //   });

    //   if (costDrivers !== undefined) {
    //     setCostDrivers(costDrivers);
    //   }
    //   // Get risk factors
    //   const riskFactors = await fetch("/api/parse-risk-factors", {
    //     method: "POST",
    //     body: JSON.stringify({
    //       messageContents: outputMessage.content,
    //     }),
    //   }).then(async (res) => {
    //     const reader = res.body?.getReader();
    //     const decoder = new TextDecoder("utf-8");
    //     let result = "";
    //     if (reader === undefined) {
    //       return;
    //     }
    //     // Read the stream
    //     while (true) {
    //       const { done, value } = await reader.read();

    //       if (done) {
    //         // The stream was fully read
    //         console.log(result);
    //         return JSON.parse(result) as RiskFactor[];
    //       }

    //       // Decode the chunk and append it to the result
    //       result += decoder.decode(value);
    //     }
    //   });

    //   if (riskFactors !== undefined) {
    //     setRiskFactors(riskFactors);
    //   }

      // Get summary
      const summary = await fetch("/api/parse-summary", {
        method: "POST",
        body: JSON.stringify({
          messageContents: outputMessage.content,
        }),
      }).then(async (res) => {
        const reader = res.body?.getReader();
        const decoder = new TextDecoder("utf-8");
        let result = "";
        if (reader === undefined) {
          return;
        }
        // Read the stream
        while (true) {
          const { done, value } = await reader.read();

          if (done) {
            // The stream was fully read
            console.log(result);
            return JSON.parse(result) as SummaryStats;
          }

          // Decode the chunk and append it to the result
          result += decoder.decode(value);
        }
      });

      console.log(summary);
      if (summary !== undefined) {
        setSummary(summary);
      }
    }
  }

  const { messages, input, handleInputChange, handleSubmit } = useChat({
    onFinish: onStreamComplete,
  });

  return (
    <div
      className="grid grid-cols-2 h-screen ml-20 mr-20"
      style={{ maxHeight: 800 }}
    >
      {" "}
      {/* h-screen to make the grid full height */}
      {/* Have one column here */}
      <div className="w-full  py-24 mx-auto bg-grey shadow-md rounded-lg text-white">
        <BasicTabs
          costDrivers={costDrivers}
          riskFactors={riskFactors}
          summary={summary}
        />
      </div>
      
      {/* Have second column here */}
      <div className="w-full  py-24 mx-auto bg-grey shadow-md rounded-lg flex flex-col">
        {" "}
        {/* flex and flex-col to make the form stick to the bottom */}
        <div
          className="overflow-y-auto p-4 flex-grow"
          style={{ maxHeight: 800, width: "100%" }}
        >
          {" "}
          {/* flex-grow to make the messages take up the remaining space */}
          {messages.length > 0
            ? messages.map((m) => (
                <div
                  key={m.id}
                  className="whitespace-pre-wrap mb-4 p-3 rounded-lg bg-blue-100 text-blue-800"
                  style={{
                    alignSelf: m.role === "user" ? "flex-end" : "flex-start",
                  }}
                >
                  <p className="font-semibold">
                    {m.role === "user" ? "User" : "AI"}
                  </p>
                  <p>{m.content}</p>
                </div>
              ))
            : null}
        </div>
        <form onSubmit={handleSubmit} className="mt-auto">
          {" "}
          {/* mt-auto to push the form to the bottom */}
          <input
            className="w-full p-2 mb-8 border border-gray-300 rounded shadow-xl bg-gray-50 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            value={input}
            placeholder="Describe your procurement problem"
            onChange={handleInputChange}
          />
        </form>
      </div>
    </div>
  );
}
