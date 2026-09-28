import os
import shutil
import kagglehub


def extract_data():

    try:
        dataset_path = kagglehub.dataset_download(
            "shiyalkishan01/indian-e-commerce-sales-and-customer-analytics"
        )

        print(f"Dataset downloaded at: {dataset_path}")

        # Check downloaded files
        print("\nAvailable files:")
        for file in os.listdir(dataset_path):
            print(" -", file)

        target_folder = "data/raw"
        os.makedirs(target_folder, exist_ok=True)

        files = [
            "customer_reviews.csv",
            "customers.csv",
            "order_items.csv",
            "orders.csv",
            "products.csv",
            "shipments.csv",
            "dataset_validation_report.csv",
            "payments.csv",
            "returns.csv",
            "data_dictionary.csv",
            "marketing_campaigns.csv"
  
        ]

        for file in files:

            source = os.path.join(dataset_path, file)
            destination = os.path.join(target_folder, file)

            if not os.path.exists(source):
                raise FileNotFoundError(
                    f"{file} not found in downloaded dataset: {dataset_path}"
                )

            shutil.copy2(source, destination)

            print(f"Copied: {file}")

        print("\nExtraction completed successfully")

    except Exception as e:
        raise RuntimeError(f"ETL Extract failed: {e}")


if __name__ == "__main__":
    extract_data()