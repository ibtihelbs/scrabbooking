import os
import pandas as pd

TODAY_FILE = "books_all.csv"
PREVIOUS_FILE = "books_previous.csv"
CHANGES_FILE = "changes.csv"

# If previous file exists, compare
if os.path.exists(PREVIOUS_FILE):
    df_prev = pd.read_csv(PREVIOUS_FILE)
    df_today = pd.read_csv(TODAY_FILE)

    merged = df_today.merge(
        df_prev,
        on="title",
        how="outer",
        suffixes=("_today", "_prev"),
        indicator=True
    )

    # new books
    new_books = merged[merged["_merge"] == "left_only"]

    # price changes
    price_changes = merged[
        (merged["_merge"] == "both") &
        (merged["price_today"] != merged["price_prev"])
    ]

    # stock changes
   
    stock_changes = merged[
        (merged["_merge"] == "both") &
        (merged["in_stock_today"] != merged["in_stock_prev"])
    ]

    changes = pd.concat([new_books, price_changes, stock_changes])
    changes.to_csv(CHANGES_FILE, index=False)

    print("New books:", len(new_books))
    print("Price changes:", len(price_changes))
    print("Stock changes:", len(stock_changes))

# overwrite previous with today
os.replace(TODAY_FILE, PREVIOUS_FILE)
