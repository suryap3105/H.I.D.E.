import argparse, importlib, pandas as pd
from hide.core.adapters import load_domain_adapter
from hide.core.ingestion import ingest_data

def main(args):
    print(f"--- Starting HIDE Training for Domain: {args.domain} ---")
    config = load_domain_adapter(args.domain)
    StrategyClass = getattr(importlib.import_module(f"hide.strategies.unified_gnn.strategy"), "UnifiedGnnStrategy")
    strategy = StrategyClass(config)
    data = ingest_data(config)
    if (isinstance(data, pd.DataFrame) and data.empty) or (isinstance(data, dict) and not data):
        print("ERROR: No data ingested. Cannot train model."); return
    strategy.execute_train(data)
    print(f"\n--- HIDE Training for Domain '{args.domain}' Complete ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HIDE Model Trainer")
    parser.add_argument("domain", help="The domain to train (dark_pools, energy_theft, etc.)")
    main(parser.parse_args())