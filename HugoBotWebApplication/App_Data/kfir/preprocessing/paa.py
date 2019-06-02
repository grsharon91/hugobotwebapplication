import pandas as pd
from tqdm import tqdm


def paa(df, window_size):
    print('performing PAA...')
    if window_size < 1:
        raise Exception('ERROR: Invalid window size parameter')

    if window_size == 1:
        return df

    for entity_id, entity_df in tqdm(df.groupby(by='EntityID')):
        for property_id, prop_df in entity_df.groupby(by='TemporalPropertyID'):
            max_time = prop_df.TimeStamp.max()
            for start_time in range(0, max_time, window_size):
                end_time = start_time + window_size
                values_in_window = prop_df[(start_time <= prop_df.TimeStamp) & (prop_df.TimeStamp < end_time)].\
                    TemporalPropertyValue

                if values_in_window.shape[0] == 0:
                    continue
                else:
                    avg = values_in_window.mean()
                    df.drop(df[
                                (start_time <= df.TimeStamp) &
                                (df.TimeStamp < end_time) &
                                (df.TemporalPropertyID == property_id) &
                                (df.EntityID == entity_id)].index, axis=0,
                            inplace=True)
                    new_ts = [entity_id, property_id, start_time, avg]
                    tmp_df = pd.DataFrame([new_ts], columns=df.columns)
                    df = df.append(tmp_df, ignore_index=True)
    return df
