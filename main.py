from analyse import *
from fetch_data import fetch_data
from visualise import *

# Example usage
if __name__ == '__main__':
    source_input = input("Enter data source (database/cloud): ").strip().lower()
    data = fetch_data(source_input)

    # if data:
    #     print("Fetched Data:")
    #     for entry in data:
    #         print(entry)
    # else:
    #     print("Failed to fetch data.")

    analysis_results = analyse(data)

    visualise(data, analysis_results)