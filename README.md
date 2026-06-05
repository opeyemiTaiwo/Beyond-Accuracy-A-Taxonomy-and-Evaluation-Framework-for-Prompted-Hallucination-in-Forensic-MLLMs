# When Accuracy Misleads: How Prompting Strategies Reshape Hallucination Profiles in MLLMs for Forensic Video Analysis

Replication package for our study of hallucination behavior in multimodal large
language models (MLLMs) applied to forensic video analysis.

We define a taxonomy of six hallucination types (H1–H6) spanning **fabrication,
omission, and distortion**, and evaluate 807 anomalous UCF-Crime videos
(annotated with the UCA dataset) across **8 prompting techniques** and **3
frontier MLLMs** (Claude Opus 4.7, GPT-5.5, Gemini 3.1 Pro). The resulting
forensic reports are cross-judged by a 3-judge LLM panel, then analyzed for
hallucination signatures, prompting effects, accuracy–safety decoupling, and
type-dependent detectability.

## Repository structure

| Path | Description |
|---|---|
| `panel_judges_FULL_v7_final.py` | Builds (ground-truth, model-output) triplets and runs the 3-judge panel; majority-vote H1–H6 labels + inter-judge agreement. |
| `complete_embeddings-final.py` | Resumable, token-budgeted embedding of model outputs (for detectability ablations). |
| `full_study_statistical_analyses_fixed.py` | Inter-judge Cohen's κ with bootstrap 95% CIs, per-crime chi-square, two-way ANOVA. |
| `full_study_ablations_fixed_FINAL.py` | Single-judge vs. panel, leave-one-out, feature ablation, training-size sweep, taxonomy-granularity comparison. |
| Prompting technique scripts | One per technique: Zero-Shot, Self-Consistency, Meta-Prompting, Chain-of-Thought, Sequential, ReAct, Least-to-Most, Iterative. |

> **Note:** model API clients and keys have been removed from the released code.
> Each model call is routed through a stub (`call_model`, `call_judge_model`,
> `embed_texts`) that you implement with your own backend and credentials.

## Hallucination taxonomy

| Code | Type | Axis |
|---|---|---|
| H1 | Scene fabrication | Fabrication |
| H2 | Crime misclassification | Distortion |
| H3 | Crime omission | Omission |
| H4 | Severity minimization | Distortion |
| H5 | Entity fabrication | Fabrication |
| H6 | Phantom actors | Fabrication |

## Requirements

- Python 3.12
- `numpy`, `pandas`, `requests`, `tqdm`
- `scikit-learn`, `scipy`, `statsmodels`
- `sentence-transformers` (optional, for local MiniLM embeddings)
- API SDKs for whichever backends you wire into the stubs

```bash
pip install -r requirements.txt
```

## Data

- **Video:** UCF-Crime (Sultani et al., 2018)
- **Annotations:** UCA dataset (Yuan et al., 2024)
- **Frames:** pre-extracted frames (Abdulrahaman et al., 2025)

Place ground-truth JSON (`UCFCrime_Train/Val/Test.json`) and saved model outputs
in the directories named at the top of each script, then run in pipeline order.

## Pipeline order

The scripts chain through CSV/NPY files on disk, so run them in this order:

1. **Generate reports** — run the prompting-technique scripts to produce model outputs.
2. **`panel_judges_FULL_v7_final.py`** — label hallucinations → `panel_raw_judge_labels_full.csv`, `all_triplets_cache.csv`.
3. **`complete_embeddings-final.py`** — embed model outputs.
4. **`full_study_statistical_analyses_fixed.py`** — κ CIs, chi-square, ANOVA.
5. **`full_study_ablations_fixed_FINAL.py`** — detectability and ablation studies.

## Reproducibility settings

- Random seed: `42` (classifier, bootstrap, all splits)
- Classifier: `LogisticRegression(max_iter=2000, class_weight='balanced')`
- Evaluation: 80/20 stratified split + 5-fold stratified CV
- Bootstrap: 1000 resamples, 95% CI
- Judge generation: `temperature=0.1`, `top_p=0.8`, `max_output_tokens=8192`

## Citation

```bibtex
@inproceedings{anonymousrepo2026,
  title     = {When Accuracy Misleads: How Prompting Strategies Reshape
               Hallucination Profiles in MLLMs for Forensic Video Analysis},
  author    = {Anonymous},
  booktitle = {Under review},
  year      = {2026}
}
```

## License

Released for research use. Video and annotation data are subject to the
licenses of their respective source datasets (UCF-Crime, UCA).
