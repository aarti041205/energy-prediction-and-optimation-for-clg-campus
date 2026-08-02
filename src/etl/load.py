def save_processed_data(df, output_path):

    df.to_csv(output_path, index=False)

    print("Processed dataset saved successfully!")