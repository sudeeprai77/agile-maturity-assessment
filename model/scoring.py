from model.maturity_model import SUB_AREAS

def calculate_area_scores(df):
    df = df.copy()
    df["normalized"] = df["score"] / 5
    result = []

    for area, subs in SUB_AREAS.items():
        subset = df[df["area"] == area]
        if subset.empty:
            continue
        score = sum(
            subset["normalized"] *
            subset["sub_area"].map(subs)
        )
        result.append((area, score * 100))

    return result
