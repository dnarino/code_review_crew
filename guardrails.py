import json

def security_review_output_guardrail(output):
    
    # get the (JSON) output from the TaskOutput object
    try: 
        json_output = output if type(output)==dict else output.json_dict 
    except Exception as e:
        return (False, ("Error retrieving the `json_dict` argument: "
                        f"\n{str(e)}\n"
                        "Make sure you set the output_json parameter in the Task."
                        )
                )

    # define risk levels
    valid_risk_levels = ['low', 'medium', 'high']
    
    # Check if security_vulnerabilities key exists
    if 'security_vulnerabilities' not in json_output:
        return (False, f"Missing 'security_vulnerabilities' key in output. Got keys: {list(json_output.keys())}")
    
    # validate that each of the risk levels has a valid value
    for vuln in json_output['security_vulnerabilities']:
        # validate the risk level
        if vuln['risk_level'].lower() not in valid_risk_levels: 
            error_message = f"Invalid risk level: {vuln['risk_level']}"
            return (False, error_message) 
    
    ### START CODE HERE ###
    # validate that the highest risk level matches the highest risk level in the vulnerabilities
    
    # if the highest risk level is not valid risk level, return an error message
    if json_output["highest_risk"].lower() not in valid_risk_levels:
        error_message = f"Invalid highest risk level: {json_output['highest_risk']}"
        return (False, error_message)
    
    # if it is one of the valid risk levels, then check if it matches the highest 
    # risk level in the vulnerabilities
    else:
        # get all risk_level values
        risk_levels = [vuln['risk_level'].lower() for vuln in json_output['security_vulnerabilities']] 
        
        # if "high" in risk levels, then highest risk level should be high
        if "high" in risk_levels: 
            if json_output["highest_risk"].lower() != "high":
                error_message = "Highest risk level does not match the highest risk level in the vulnerabilities." 
                return (False, error_message)
            
        # if high is not present and medium is in risk levels, then highest risk level should be medium
        elif "medium" in risk_levels: 
            if json_output["highest_risk"].lower() != "medium":
                error_message = "Highest risk level does not match the highest risk level in the vulnerabilities." 
                return (False, error_message)
            
        # if high and medium are not present, then lowest risk level should be low
        elif "low" in risk_levels: 
            if json_output["highest_risk"].lower() != "low":
                error_message = "Highest risk level does not match the highest risk level in the vulnerabilities." 
                return (False, error_message)
    
    ### END CODE HERE ###

    return (True, output.json_dict)

# create the output json for testing
invalid_json = {"highest_risk": "medium", 
                "security_vulnerabilities": [
                        {"risk_level": "high"}, 
                        {"risk_level": "medium"}
                    ]
                }
# test the guardrail
#security_review_output_guardrail(invalid_json)

#print(security_review_output_guardrail(invalid_json))


def review_decision_guardrail(output): 
    try:
        output= output  if type(output)== str else output.raw 
    except Exception as e:
        return(False,("Error retrieving the `raw` argument: "
                        f"\n{str(e)}\n"
                        "Make sure you set the raw parameter in the Task."
                        ) 
                )
   #define the keywords to check for in the output
    keywords=["approve","request changes","escalate"]
    if not any(keyword in output.lower() for keyword in keywords):
        error_message = "'Output does not include one of the valid actionable decisions.'"
        return (False , error_message)
    return (True, output)

#test guardrail
#input='Final decision: escalate, Elevate to human'
#review_decision_guardrail(input)¨