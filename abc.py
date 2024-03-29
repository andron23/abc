import numpy as np
import pandas as pd
import plotly.express as px

# Считываем данные
df = pd.read_csv(
    "abc2.csv",
    sep=";",
    decimal=",",
)

# Проводим многомерный ABC-анализ по выручке, количеству и прибыльности
index = "name"
cols = list(df.columns)
cols.remove(index)
for col in cols:
    groupped_df[f"rel_{col}"] = groupped_df[col] / sum(groupped_df[col])
    groupped_df = groupped_df.sort_values(f"rel_{col}", ascending=False)
    groupped_df[f"cumsum_{col}"] = groupped_df[f"rel_{col}"].cumsum()
    groupped_df[f"abc_{col}"] = np.where(
        groupped_df[f"cumsum_{col}"] < 0.8,
        "A",
        np.where(groupped_df[f"cumsum_{col}"] < 0.95, "B", "C"),
    )

# Сохраняем результат
groupped_df[cols + [f"abc_{col}" for col in cols]].to_excel("1.xlsx", index=False)


# Формируем итоговые наборы групп
groupped_df["final_group"] = (
    groupped_df["abc_revenue"] + groupped_df["abc_amount"] + groupped_df["abc_profit"]
)
groups = groupped_df.groupby("final_group")["final_group"].agg({"count"}).reset_index()
groups["perc"] = groups["count"] / sum(groups["count"])

# Код для построения графика treemap
fig = px.treemap(groups, path=["final_group"], values="perc")
fig.show()
