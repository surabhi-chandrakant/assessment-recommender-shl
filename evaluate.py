"""
Evaluation Script: Compute Recall@K on training data
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from recommender import SHLRecommender, normalize_url
import openpyxl
from collections import defaultdict
import numpy as np

def load_train_data(excel_path):
    """Load training data from Excel."""
    wb = openpyxl.load_workbook(excel_path)
    ws = wb['Train-Set']
    
    query_labels = defaultdict(list)
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] and row[1]:
            query_labels[row[0]].append(row[1])
    
    return dict(query_labels)

def evaluate(excel_path, data_path, k=10):
    """Full evaluation pipeline."""
    print("Loading training data...")
    query_labels = load_train_data(excel_path)
    print(f"Loaded {len(query_labels)} unique queries with labels")
    
    print("\nLoading recommender...")
    rec = SHLRecommender(data_path=data_path)
    rec.load()
    
    print(f"\nEvaluating Recall@{k}...")
    recalls = []
    
    for query, relevant_urls in query_labels.items():
        recommendations = rec.recommend(query, top_k=k)
        
        # Normalize URLs for comparison (handle /solutions/ vs without)
        rec_urls = set()
        for r in recommendations:
            url = r['url'].rstrip('/')
            rec_urls.add(url)
            rec_urls.add(url.replace('/solutions/products/', '/products/'))
            rec_urls.add(url.replace('/products/', '/solutions/products/'))
        
        rel_urls = set()
        for u in relevant_urls:
            u = u.rstrip('/')
            rel_urls.add(u)
            rel_urls.add(u.replace('/solutions/products/', '/products/'))
            rel_urls.add(u.replace('/products/', '/solutions/products/'))
        
        # Count hits (how many relevant are in recommendations)
        # Use original relevant_urls count
        unique_rel = set(normalize_url(u) for u in relevant_urls)
        unique_rec = set()
        for r in recommendations:
            u = normalize_url(r['url'])
            unique_rec.add(u)
            # Also add alternate forms
            unique_rec.add(u.replace('/solutions/products/', '/products/'))
            unique_rec.add(u.replace('/products/', '/solutions/products/'))
        
        hits = len(rel_urls & rec_urls)
        recall = hits / len(relevant_urls)
        recalls.append(recall)
        
        print(f"\nQuery: {query[:70]}...")
        print(f"  Relevant: {len(relevant_urls)}, Hits: {hits}, Recall@{k}: {recall:.3f}")
        print(f"  Top 5 recommendations:")
        for r in recommendations[:5]:
            marker = "✓" if any(
                normalize_url(r['url']) in normalize_url(rel_u) or 
                normalize_url(rel_u) in normalize_url(r['url']) 
                for rel_u in relevant_urls
            ) else " "
            print(f"    [{marker}] {r['name']} | score={r['_score']:.3f}")
    
    mean_recall = np.mean(recalls)
    print(f"\n{'='*60}")
    print(f"MEAN RECALL@{k}: {mean_recall:.4f}")
    print(f"{'='*60}")
    
    return mean_recall

if __name__ == "__main__":
    excel_path = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/uploads/Gen_AI_Dataset__2_.xlsx"
    data_path = sys.argv[2] if len(sys.argv) > 2 else "data/shl_assessments.json"
    
    evaluate(excel_path, data_path)
