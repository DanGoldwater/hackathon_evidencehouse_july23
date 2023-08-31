import textwrap

from backend.llm_inference import create_chat_completion

output_message = """
Cost Drivers:

Title: Equipment Cost

Cost: High
Description: The cost of purchasing the 10 fmri machines will be a significant cost driver in this procurement. The pricing of the machines can vary based on specifications, brand, and supplier agreements.
Title: Installation and Training

Cost: Moderate
Description: Proper installation and training are essential for the effective utilization of fmri machines. Costs associated with installation, calibration, and training of staff members would contribute to the overall expenditure.
Title: Maintenance and Service

Cost: Moderate to High
Description: Regular maintenance and servicing are crucial to ensure the continuous and reliable operation of fmri machines. Costs related to preventive maintenance, repairs, and replacement of parts should be considered.
Risks:

Title: Regulatory Changes

Description: Changes in regulatory requirements related to medical devices and protocols can impact the procurement process, leading to additional costs for compliance and possible delays.
Cost: Moderate
Likelihood: Moderate
Impact: Moderate
Title: Supplier Reliability

Description: The reliability and reputation of the chosen supplier can influence the overall success of the procurement. In case of delays, poor after-sales support, or inability to deliver as promised, there might be additional costs associated with finding alternative solutions.
Cost: High
Likelihood: Moderate
Impact: High
Title: Technological Obsolescence

Description: The fast-paced nature of technology advancements could render the fmri machines outdated in a relatively short period. There is a risk of the machines becoming obsolete before expected, leading to extra costs for upgrades or replacements.
Cost: Moderate
Likelihood: High
Impact: Moderate
Summary:
The cost drivers for this procurement predominantly include the equipment cost, installation and training expenses, and ongoing maintenance and service costs. The key risks identified are regulatory changes, supplier reliability, and technological obsolescence. Considering these drivers and risks, it is important to carefully analyze supplier options, evaluate service agreements, and plan for long-term maintenance and upgrades to ensure successful and cost-effective procurement of the fmri machines for the NHS.
"""
response = create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": "You are a data analyst in charge of assisting the UK government with procurement of contracts",
        },
        {
            "role": "user",
            "content": textwrap.dedent(
                f"""
                Your job is to extract the risk factors from this message as a list of json objects: {output_message}.
                The format of the json objects should be:
                [
                    {{
                        "title": "itle of risk factor",
                        "cost": "cost of cost driver",
                        "description": "description of risk factor",
                        "probability": "probability of risk factor"
                    }},
                ]
                ensure the answer is parsable using json.loads(answer) return nothing else
                """
            ),
        },
    ],
)
output = ""
for x in response:
    output += x

print(output)
