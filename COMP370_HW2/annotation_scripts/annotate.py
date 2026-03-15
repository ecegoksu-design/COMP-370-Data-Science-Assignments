import pandas as pd

def main():
    df = pd.read_csv('cleaned_pony_dialogue.csv')
    
    df['addressee'] = df.groupby('episode')['speaker'].shift(-1)
    df['addressee'] = df['addressee'].fillna('nobody')
    
    df.to_csv('annotated_pony_dialogue.csv', index=False)

if __name__ == '__main__':
    main()