import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { CostDriver, RiskFactor, SummaryStats } from "@/app/page";
import { BoxPlot } from "./BoxPlot";
import BarChart from "./BarChart";

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    "aria-controls": `simple-tabpanel-${index}`,
  };
}

export interface Tabs {
  costDrivers: CostDriver[];
  riskFactors: RiskFactor[];
  summary: SummaryStats;
}

export default function BasicTabs(props: Tabs) {
  const [value, setValue] = React.useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: "100%" }}>
      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Tabs
          value={value}
          onChange={handleChange}
          aria-label="basic tabs example"
          className="text-white"
        >
          <Tab label={"Overview"} sx={{ color: "white" }} {...a11yProps(0)} />
          <Tab
            label={"Costs Drivers"}
            sx={{ color: "white" }}
            {...a11yProps(1)}
          />
          <Tab
            label={"Risk Factors"}
            sx={{ color: "white" }}
            {...a11yProps(2)}
          />
        </Tabs>
      </Box>
      <CustomTabPanel value={value} index={0}>
        <div className="flex flex-col">
          {props.summary.overview === undefined ? (
            <div className="flex flex-col">
              <div style={{ fontSize: "20px" }}>
                <b>
                  <p>Please Enter A project</p>
                </b>
                <br />
              </div>
            </div>
          ) : (
            <div>
              <h1 className="text-large">Overview</h1>
              <p>{props.summary.overview}
        {props.summary.similairProjects.length}
              
              </p>
              <hr />

              <BoxPlot
                label={"Costs"}
                data={[
                  { min: 100, q1: 200, median: 300, q3: 400, max: 500 },
                  { min: 200, q1: 300, median: 400, q3: 500, max: 600 },
                ]}
              />
              <h1>Similair Projects</h1>
              {props.summary.similairProjects.map((project) => (
                <div>
                  <div className="flex flex-col">
                    <div style={{ fontSize: "20px" }}>
                      <b>
                        {project.name}
                        <span style={{ color: "green", marginLeft: "10px" }}>
                          {" "}
                          {/* Display in millions if long enough otherwise thousands */}
                          Expected Cost: ${project.expectedCost}
                        </span>
                        <span style={{ color: "green", marginLeft: "10px" }}>
                          {" "}
                          {/* Display in millions if long enough otherwise thousands */}
                          Actual Cost: ${project.actualCost}
                        </span>
                      </b>
                      <br />
                    </div>
                    <div
                      className="mt-5"
                      style={{
                        fontSize: "18px",
                        marginBottom: "15px",
                        marginTop: "20px",
                      }}
                    >
                      Timeframe:
                      {project.timeframe}
                    </div>
                    <hr />
                    <br />
                  </div>
                </div>
              ))}

              {/* <BarChart
                labels={
                  props.summary.similairProjects.map(
                    (project) => project.name
                  ) || []
                }
                data={
                  props.summary.similairProjects.map(
                    (project) => project.timeframe
                  ) || []
                }
              /> */}
            </div>
          )}
          {/* TODO add summary stats here */}
        </div>
      </CustomTabPanel>
      <CustomTabPanel value={value} index={1}>
        {props.costDrivers.map((costDriver) => (
          <div className="flex flex-col">
            <div style={{ fontSize: "20px" }}>
              <b>
                {costDriver.title}
                <span style={{ color: "green", marginLeft: "10px" }}>
                  {" "}
                  {/* Display in millions if long enough otherwise thousands */}
                  Cost Range: ${costDriver.minCost / 1_000_000}M -{" "}
                  {costDriver.maxCost / 1_000_000}M
                </span>
              </b>
              <br />
            </div>
            <div
              className="mt-5"
              style={{
                fontSize: "18px",
                marginBottom: "15px",
                marginTop: "20px",
              }}
            >
              {costDriver.description}
            </div>
            <hr />
            <br />
          </div>
        ))}
        <BarChart
          data={props.costDrivers.map((costDriver) => costDriver.maxCost) || []}
          labels={props.costDrivers.map((costDriver) => costDriver.title) || []}
        />
      </CustomTabPanel>
      <CustomTabPanel value={value} index={2}>
        {props.riskFactors.map((riskFactor) => (
          <div className="flex flex-col mt-5">
            <div style={{ fontSize: "20px" }}>
              <b>
                {riskFactor.title}
                <span style={{ color: "red", marginLeft: "10px" }}>
                  {" "}
                  Risk: {riskFactor.likelihood}
                </span>
                <span style={{ color: "green", marginLeft: "10px" }}>
                  {" "}
                  Cost Range: ${riskFactor.minCost / 1_000_000}M -{" "}
                  {riskFactor.maxCost / 1_000_000}M
                </span>
              </b>
              <br />
            </div>
            <div
              className="mt-5"
              style={{
                fontSize: "18px",
                marginBottom: "15px",
                marginTop: "20px",
              }}
            >
              {riskFactor.description}
            </div>
            <hr />
            <br />
          </div>
        ))}
      </CustomTabPanel>
    </Box>
  );
}
