"""
Generate Test Set Predictions
Usage: python generate_predictions.py <excel_path> <output_csv>
"""
import sys
import os
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from recommender import SHLRecommender
import openpyxl


def generate_predictions(excel_path, output_csv, data_path="data/shl_assessments.json"):
    print("Loading recommender...")
    rec = SHLRecommender(data_path=data_path)
    rec.load()

    print("Loading test queries...")
    wb = openpyxl.load_workbook(excel_path)
    ws = wb['Test-Set']
    queries = [row[0] for row in ws.iter_rows(min_row=2, values_only=True) if row[0]]
    print(f"Found {len(queries)} test queries")

    predictions = []
    for i, query in enumerate(queries):
        results = rec.recommend(query, top_k=10)
        print(f"Query {i+1}: {query[:70]}...")
        for r in results:
            predictions.append({"Query": query, "Assessment_url": r["url"]})
        print(f"  -> {len(results)} recommendations")

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Query", "Assessment_url"])
        writer.writeheader()
        writer.writerows(predictions)

    print(f"\nSaved {len(predictions)} rows to {output_csv}")
    return predictions


if __name__ == "__main__":
    excel = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/uploads/Gen_AI_Dataset__2_.xlsx"
    output = sys.argv[2] if len(sys.argv) > 2 else "predictions.csv"
    generate_predictions(excel, output)
