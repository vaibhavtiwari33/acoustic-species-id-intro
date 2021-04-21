def stratify_datafile(filepath):    
    df = pd.read_csv(filepath)
    df = df[(df['AudioMothCode'].notna()) & 
            (df['Duration'].notna()) & 
            (df['Comment'].notna()) & 
            (df['FileSize'].notna()) &
            (df['Duration'] >= 60.0) &
            (df['FileSize'] >= 46080192)]
    
    df['hour'] = df['Comment'].apply(lambda x: datetime.strptime(' '.join(x.split()[2:4]), 
                                                                 '%H:%M:%S %d/%m/%Y'))\
                              .dt\
                              .hour\
                              .tolist()
    
    df = df.groupby(["AudioMothCode", "hour"])\
           .apply(lambda x: x.sample(1))\
           .drop(columns='hour')
    
    if df.size > 0:
        df.to_csv(filepath.replace('.csv', '_stratified.csv'), index=False)
        return True
    return False
