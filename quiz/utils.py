import ast


def convert_to_list(string_list):
    try:
        # Use ast.literal_eval to safely evaluate the string
        result = ast.literal_eval(string_list)

        # Check if the result is a list of integers
        if isinstance(result, list) and all(isinstance(item, int) for item in result):
            return result
    except (ValueError, SyntaxError) as e:
        return []
