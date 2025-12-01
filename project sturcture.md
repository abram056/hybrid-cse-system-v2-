hybrid-cse-system/
│
├── README.md
├── requirements.txt
├── pyproject.toml          # optional if using poetry/pipenv
│
├── config/
│   ├── training.yaml
│   ├── model.yaml
│   └── paths.yaml
│
├── data/
│   ├── raw/
│   │   ├── smish/
│   │   ├── spam/
│   │   ├── convo/
│   │   ├── adversarial/
│   │   └── synthetic/
│   │
│   ├── processed/
│   │   ├── train.csv
│   │   ├── test.csv
│   │   └── validation.csv
│   │
│   └── external/
│       └── (any licensed datasets, e.g. switchboard if restricted)
│
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_phase1_conversation_finetune.ipynb
│   ├── 03_phase2_fraud_finetune.ipynb
│   ├── 04_hybrid_testing.ipynb
│   └── legacy_v1_reference.ipynb    # optional for comparing with old project
│
├── src/
│   ├── __init__.py
│   │
│   ├── data/
│   │   ├── load.py
│   │   ├── preprocess.py
│   │   ├── build_dataset.py
│   │   └── augment.py
│   │
│   ├── models/
│   │   ├── rbs/
│   │   │   ├── suspicious_message_engine.py
│   │   │   ├── wordlists/
│   │   │   │   ├── suspicious_words.txt
│   │   │   │   └── suspicious_phrases.txt
│   │   │   └── __init__.py
│   │   │
│   │   ├── bert/
│   │   │   ├── train_phase1.py
│   │   │   ├── train_phase2.py
│   │   │   ├── classifier_head.py
│   │   │   └── inference.py
│   │   │
│   │   ├── hybrid/
│   │   │   ├── meta_classifier.py     # merges RBS + BERT
│   │   │   └── pipeline.py            # unified prediction interface
│   │   │
│   │   └── __init__.py
│   │
│   ├── evaluation/
│   │   ├── metrics.py
│   │   ├── confusion_matrix.py
│   │   └── adversarial_eval.py
│   │
│   └── api/
│       ├── fastapi_app.py
│       └── schema.py
│
├── experiments/
│   ├── trial_01/
│   ├── trial_02/
│   └── saved_models/
│       ├── distilbert_conversational/
│       ├── cse_fraud_bert/
│       └── hybrid_cse_system/
│
└── scripts/
    ├── run_phase1.sh
    ├── run_phase2.sh
    ├── run_hybrid.sh
    └── benchmark.py

