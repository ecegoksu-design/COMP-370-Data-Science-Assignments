import pandas as pd
import re

# Content cleaning method
def clean_content(text):
    if pd.isna(text):
        return text
    text = re.sub(r'\[.*?\]', '', text)  
    text = re.sub(r'\(.*?\)', '', text)  
    text = re.sub(r'\s+', ' ', text)     
    return text.strip()

def main():
    df = pd.read_csv('archive/clean_dialog.csv')
    
    df = df.rename(columns={'title': 'episode', 'pony': 'speaker', 'dialog': 'content'})
    
    df['content'] = df['content'].apply(clean_content)
    
    # Save cleaned, renamed data
    df.to_csv('cleaned_pony_dialogue.csv', columns=['episode', 'speaker', 'content'], index=False)
    
    # Run a sample check for issues
    sample = df.sample(n=100, random_state=42)
    issues = sample[sample['content'].isna() | (sample['content'] == '') | sample['speaker'].isna() | (sample['speaker'] == '')]
    if not issues.empty:
        print("Issues found in cleaned data:")
        print(issues)
    else:
        print("No issues in the sample.")

if __name__ == '__main__':
    main()