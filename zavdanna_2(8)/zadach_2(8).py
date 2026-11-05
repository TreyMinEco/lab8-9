import matplotlib.pyplot as plt
import pandas as pd

def load_f(filename):
    try:
        df = pd.read_csv(filename, parse_dates=["Date"], dayfirst=True, index_col="Date")
        print("File yspishno vidcrito")
        return df
    except FileNotFoundError:
        print("Error, file ne znaydeno!")
        return None
    except Exception as e:
        print("Error:", e)
        return None


def analysis(df):
    if df is None:
        print("Error, work program finish!")
        return

    print("\nPochatkovi dani:")
    print(df)
    print("\nPershi 3 radka:")
    print(df.head(3))
    print("\nType data:")
    print(df.dtypes)
    print("\nRozmir DataFrame:")
    print(df.shape)
    print("\nStats:")
    print(df.describe())

def obrobka_data(df):
    if df is None:
        print("Error, dani ne proanalizovano!")
        return None

    try:
        df = df.select_dtypes(include="number").copy()

        total_cyclists = df.sum().sum()
        print(f"\nZagalna kilkist velo: {int(total_cyclists)}")

        date_index = pd.to_datetime(df.index, dayfirst=True)
        month_names = date_index.strftime("%b")
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        df["Month"] = pd.Categorical(month_names, categories=month_order, ordered=True)
        return df
    except Exception as e:
        print("Error v obrobci danih:", e)
        return None

def filtr_data(df):
    if df is None:
        print("Error ne mae danih!")
        return None

    if "Berri1" in df.columns:
        filtr_d = df[df["Berri1"] > 5000]
        print("\nDani de Berri1 > 5000:")
        print(filtr_d)
        return filtr_d
    else:
        print("Stovpec Berri1 ne znaydeno для фільтрації!")
        return None

def group_data(df):
    if df is None:
        print("Error ne mae danih dlya grupuvannya!")
        return None

    paths = ["Berri1", "Rachel / Papineau", "Maisonneuve_2"]
    available_paths = [p for p in paths if p in df.columns]

    if available_paths:
        grouped_df = df.groupby("Month", observed=False)[available_paths].sum()
        print("\nResult grup po misyacyah:")
        print(grouped_df)
        return grouped_df
    else:
        print("Vkazani dorizhki ne znaydeni для групування!")
        return None

def draw_plot(df, chosen_path):
    if df is None:
        print("Error ne mae danih dlya grafika!")
        return

    if chosen_path in df.columns:
        dynamics = df.groupby("Month", observed=False)[chosen_path].sum()
        dynamics.plot(kind="bar")
        plt.title(f"Status for {chosen_path}")
        plt.xlabel("Month")
        plt.ylabel("Count")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.show()
        print(f"\nGrafik dlya {chosen_path} pobudovano!")
    else:
        print(f"Error: path {chosen_path} ne znaydeno dlya grafika!")

def save_file(df, filt_d, group_d):
    try:
        if df is not None:
            df.to_csv("velo_proc.csv", encoding="utf-8")
        if filt_d is not None:
            filt_d.to_csv("velo_filter.csv", encoding="utf-8")
        if group_d is not None:
            group_d.to_csv("velo_group.csv", encoding="utf-8")
        print("\nFile saved!")
    except Exception as e:
        print("Error file ne saved:", e)


def main():
    my_df = load_f("comptagevelo2011.csv")

    if my_df is None or my_df.empty:
        print("Program finish!")
        return

    analysis(my_df)
    my_df = obrobka_data(my_df)
    if my_df is None or my_df.empty:
        print("Error obrobki danih!")
        return

    filt_d = filtr_data(my_df)
    group_d = group_data(my_df)
    draw_plot(my_df, "Berri1")
    save_file(my_df, filt_d, group_d)

main()