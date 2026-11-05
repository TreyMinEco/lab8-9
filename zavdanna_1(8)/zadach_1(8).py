import pandas as pd

def load_f(filename):
    try:
        df = pd.read_csv(filename)
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
        return None, None

    inflation = "Inflations (%)"

    try:
        df[inflation] = pd.to_numeric(df[inflation], errors="coerce")
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        df = df.dropna(subset=[inflation]).copy()
        average = df[inflation].mean()
        df["Inflation_deviation"] = df[inflation] - average
        return df, inflation

    except KeyError as e:
        print("Error, stovpec ne znaydeno:", e)
        return None, None
    except Exception as e:
        print("Error, v obrobci danih:", e)
        return None, None

def filtr_data(df, inflation):
    if df is None or inflation is None:
        print("Error ne mae danih!")
        return None

    filtr_d = df[df[inflation] > 5]
    print("\nCountry z inflation > 5:")
    print(filtr_d)
    return filtr_d

def sort_data(df, inflation):
    if df is None or inflation is None:
        print("Error ne mae danih dlya sort!")
        return None

    sort_df = df.sort_values(by=inflation, ascending=False)
    print("\nDani vidsortovano:")
    print(sort_df)
    return sort_df

def znach_lvl(znach):
    if znach < 0:
        return "Def."
    elif znach < 5:
        return "Low. inf."
    elif znach < 10:
        return "Med. inf."
    else:
        return "High inf."

def group_data(df, inflation):
    if df is None or inflation is None:
        print("Error ne mae danih dlya grupuvannya!")
        return None

    df = df.copy()
    df["Category"] = df[inflation].apply(znach_lvl)
    grouped_df = df.groupby("Category")[inflation].agg(["mean", "max", "min", "count"])
    print("\nResult grup:")
    print(grouped_df)
    return grouped_df

def kilkist_c(df):
    if "Country Name" in df.columns:
        kilkist = df["Country Name"].nunique()
    elif "Country" in df.columns:
        kilkist = df["Country"].nunique()
    else:
        print("Country stovpec ne znaydeno!")
        return 0
    print("\nKilkist country:", kilkist)
    return kilkist

def save_file(df, filt_d, sort_d, group_d):
    try:
        df.to_csv("inflation_proc.csv", index=False, encoding="utf-8")
        filt_d.to_csv("inflation_filter.csv", index=False, encoding="utf-8")
        sort_d.to_csv("inflation_sort.csv", index=False, encoding="utf-8")
        group_d.to_csv("inflation_group.csv", encoding="utf-8")
        print("\nFile saved!")
    except Exception as e:
        print("Error file ne saved:", e)

def main():
    my_df = load_f("inflation_2016.csv")

    if my_df is None or my_df.empty:
        print("Program finish!")
        return

    analysis(my_df)
    my_df, obr_d = obrobka_data(my_df)
    if my_df is None or my_df.empty:
        print("Error obrobki danih!")
        return
    print("\nData pislya obrobki:")
    print(my_df)
    filt_d = filtr_data(my_df, obr_d)
    sort_d = sort_data(my_df, obr_d)
    group_d = group_data(my_df, obr_d)
    kilkist_country = kilkist_c(my_df)
    save_file(my_df, filt_d, sort_d, group_d)

main()