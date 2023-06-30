

def format_api_result(api_result):
    # Extract the relevant information from the API result
    result_message = api_result['result'][0][0]
    probability = api_result['result'][1]

    # Format the result message with the probability
    formatted_message = f'{result_message} {probability}.'

    return formatted_message


