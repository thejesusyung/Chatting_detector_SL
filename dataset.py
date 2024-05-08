import pandas as pd
def split_into_parts(text, num_parts=100):
    # Calculate length of each part, rounded down
    part_length = len(text) // num_parts
    # Create list of parts
    parts = [text[i:i + part_length] for i in range(0, len(text), part_length)]
    return parts[:num_parts] 
def replace_newlines(strings):
    # Replace '\n' with ' ' in each string in the list
    return [s.replace('\n', ' ') for s in strings]

df = pd.read_csv('tinder_output.csv')
tinder_cases = df['Extracted Text'].to_list()
tinder_cases = replace_newlines(tinder_cases)
df_2 = pd.read_csv('translated_output.csv')
story_romantic = df_2['Translated Text'][0]
list_romantic = split_into_parts(story_romantic)
tinder_cases.extend(list_romantic)