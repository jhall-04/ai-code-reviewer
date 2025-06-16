def format_diff_prompt(filename: str, status: str, patch: str) -> str:
    """
    Format the diff information into a prompt for the AI model.
    """
    response = """
{
'comments': {
    'filename': 'name of file',
    'line': 'line where the comment should be inserted, e.g. "1"',
    'comment': 'your comment on the line'
}
'summary': 'your overall summary of the changes'
}
    """
    return f"""
You are a senior software engineer reviewing a pull request.

File: {filename}
Status: {status}

here is the code diff:

{patch}

Please identify potential issues, suggest improvements, and evaluate the overall quality of the change.
Respond with only a JSON containing the following fields:
{response}
    """