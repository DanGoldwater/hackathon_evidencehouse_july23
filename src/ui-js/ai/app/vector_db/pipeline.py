from vector_store import get_nearest_rows_from_df, get_strucutred_text_from_small_df, get_main_df
from embellish import embellish_dataframe


def run(query:str):
    df = get_nearest_rows_from_df(query, get_main_df(), top_k=5)
    df = embellish_dataframe(df)
    string_out = get_strucutred_text_from_small_df(df)
    return string_out