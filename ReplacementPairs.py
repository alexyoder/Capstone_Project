import pandas as pd

def detect_substitutions(df):
    """
    Identifies substitution pairs in the same order where:
      - A line with an item number ending in '0' is followed by a line ending in '1'
      - Both lines belong to the same order
      - Captures key fields including Material, Description, Quantity, and Rejected Item Status.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing order data with at least the following columns:
                           'Order', 'Item Number', 'Material', 'Material Description', 
                           'Order Qty', 'Rejected Item Status'
    
    Returns:
        pd.DataFrame: A DataFrame listing detected substitution pairs with detailed comparisons.
    """
    substitution_pairs = []

    # Convert 'Item Number' to integer and 'Order' to string (if not already)
    df['Item Number'] = df['Item Number'].astype(int)
    df['Order'] = df['Order'].astype(str)

    # Group the data by Order
    for order_id, group in df.groupby('Order'):
        group = group.sort_values('Item Number')
        for _, row in group.iterrows():
            item_number = row['Item Number']
            # Check if the item number ends with 0 (e.g., 10, 20, 30, etc.)
            if item_number % 10 == 0:
                # Look for the next sequential item (e.g., 10 -> 11)
                match_row = group[group['Item Number'] == item_number + 1]
                if not match_row.empty:
                    original = row
                    replacement = match_row.iloc[0]
                    substitution_pairs.append({
                        'Order': order_id,
                        'From_Item': item_number,
                        'To_Item': item_number + 1,
                        'From_Material': original['Material'],
                        'To_Material': replacement['Material'],
                        'From_Description': original['Material Description'],
                        'To_Description': replacement['Material Description'],
                        'From_Qty': original['Order Qty'],
                        'To_Qty': replacement['Order Qty'],
                        'Rejected_Status': original['Rejected Item Status']
                    })

    return pd.DataFrame(substitution_pairs)

# Main block for testing the function
if __name__ == "__main__":
    # Load your data file '10to11.csv'
    try:
        df = pd.read_csv('10to11.csv')
    except FileNotFoundError:
        print("Error: '10to11.csv' file not found. Ensure it is in the same directory as this script.")
    else:
        # Run the substitution detection function
        substitutions_df = detect_substitutions(df)
        # Display the first few detected substitution pairs
        print(substitutions_df.head())
        # Optional: Save the output to a new CSV file
        substitutions_df.to_csv('detected_substitutions.csv', index=False)