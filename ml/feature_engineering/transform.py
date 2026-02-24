
import pandas as pd

def calculate_stress_score(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.copy()
    df["stress_score"] = 0

    df.loc[df["rpm"] > 5000, "stress_score"] += 2
    df.loc[df["battery_temp"] > 95, "stress_score"] += 2
    df.loc[df["fuel_level"] < 10, "stress_score"] += 1
    df.loc[df["speed"] > 110, "stress_score"] += 1

    return df
