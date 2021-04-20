import pandas as pd
from datetime import datetime

def stratify_datafile(filepath):
    df = pd.read_csv(filepath)
    df['hour'] = df['StartDateTime'].dropna()\
                                    .apply(lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M").hour)

    audio_moths = df['AudioMothCode'].unique()
    hour_list = df['hour'].dropna().unique()

    stratified_df = pd.DataFrame(columns=df.columns)

    df = df[(df['AudioMothCode'].notna()) &
            (df['Duration'].notna()) &
            (df['hour'].notna()) &
            (df['FileSize'].notna()) &
            (df['Duration'] >= 60.0) &
            (df['FileSize'] >= 46080360) &
            (df['hour'].isin(hour_list))]

    for am in audio_moths:
        for hour in hour_list:
            temp_df = df[(df['AudioMothCode'] == am) & (df['hour'] == hour)]
            if temp_df.size > 0:
                stratified_df = pd.concat([stratified_df, temp_df.sample(n=1)])

    if stratified_df.size > 0:
        stratified_df.drop(columns='hour')\
                     .to_csv(filepath.replace('.csv', '_stratified.csv'), index=False)
        return True
    return False


stratify_datafile('Peru_2019_AudioMoth_Data_Full.csv')
