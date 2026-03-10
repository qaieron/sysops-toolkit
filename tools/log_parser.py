import argparse
import json
from datetime import datetime
import sys
import os

def parse_log(filepath):
    findings = [] # list of dictionaries, each containing the line number, severity, and message of a finding

    if not os.path.exists(filepath):
        print(f"Error: file '{filepath}' not found", file=sys.stderr)
        sys.exit(1) # exit the program with an error code if the file is not found

    with open(filepath, "r") as f: # open the file and read it line by line using enumerate to get the line number and the line itself 
        for line_number, line in enumerate(f, start=1): # start the line number at 1  
            if "ERROR" in line: # if the line contains "ERROR", add the line number, severity, and message to the findings list
                findings.append({"line_number": line_number, "severity": "ERROR", "message": line.split("] ")[-1].strip()})
            if "WARN" in line: # same for "WARN"
                findings.append({"line_number": line_number, "severity": "WARN", "message": line.split("] ")[-1].strip()})



    total_errors = sum(1 for f in findings if f["severity"] == "ERROR") # count the number of errors by iterating through the findings list and checking if the severity is "ERROR"
    total_warnings = sum(1 for f in findings if f["severity"] == "WARN") # same for "WARN"

    return {
        "generated_at": datetime.now().isoformat(), # get the current date and time and format it as an ISO string ex. 2026-03-10T13:34:15.689835
        "total_errors": total_errors, # count the number of errors
        "total_warnings": total_warnings, # count the number of warnings
        "findings": findings # return the findings list
    }

if __name__ == "__main__": # main function to run the program if the file is run directly (python log_parser.py --file sample_data/sample.log --output report.json)
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True) # add the file argument to the parser
    parser.add_argument("--output", default="report.json") # add the output argument to the parser with a default value of "report.json"
    args = parser.parse_args() # parse the arguments

    result = parse_log(args.file) # parse the log file
    with open(args.output, "w") as f: # open the output file and write the result to it
        f.write(json.dumps(result, indent=4)) # write the result to the file in a pretty format