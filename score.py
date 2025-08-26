import pandas as pd, importlib, argparse
from hide.core.ingestion import ingest_data
from hide.core.adapters import load_domain_adapter
from hide.core.reporting import create_html_report

class HidePredictor:
    def __init__(self, domain_name: str):
        self.config = load_domain_adapter(domain_name)
        StrategyClass = getattr(importlib.import_module("hide.strategies.unified_gnn.strategy"), "UnifiedGnnStrategy")
        self.strategy = StrategyClass(self.config)
    def predict(self, X): return self.strategy.execute_predict(X)

def main(args):
    print(f"\n--- HIDE PREDICTION for domain: {args.domain} ---")
    predictor = HidePredictor(args.domain)
    # In a real scenario, this would be new, unseen data. For this test, we re-ingest.
    new_data = ingest_data(predictor.config)
    if not isinstance(new_data, dict) and new_data.empty:
        print("Could not load test data."); return
        
    results_df = predictor.predict(new_data)
    
    print("\n--- Prediction Results ---")
    if results_df.empty:
        print("No anomalies or high-priority items were detected.")
    else:
        print(results_df)
        html = create_html_report(results_df.to_dict('records'), predictor.config)
        report_path = f"reports/hide_report_{args.domain}.html"
        with open(report_path, 'w') as f:
            f.write(html)
        print(f"\n-> Full report saved to {report_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="HIDE Predictor")
    parser.add_argument("domain", help="The domain to run prediction for.")
    main(parser.parse_args())