def print_table(title: str, df):
    print("\n" + title)
    print("=" * len(title))
    print(df.to_string())

def print_tables(tables):
    for title, df in tables:
        print("\n" + title)
        print("=" * len(title))
        print(df.to_string())
