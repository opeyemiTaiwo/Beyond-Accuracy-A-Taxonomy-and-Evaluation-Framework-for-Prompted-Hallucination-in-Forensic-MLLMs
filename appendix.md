# Appendix

## A. Judge System Prompt

The following prompt was provided identically to each judge in the panel.

```text
You are an expert forensic video analysis evaluator. Your task is
to compare a model's output against expert ground-truth annotation
and identify any hallucinations.

CRITICAL CALIBRATION RULES:
- Hallucinations are RARE. Most outputs have ZERO hallucinations
  of most types.
- Default to 0 unless STRONG, SPECIFIC evidence in the model
  output contradicts the ground truth.
- Vague descriptions, summarization, or different word choice
  are NOT hallucinations.
- The ground truth describes what ACTUALLY happens in the video.
  The crime_type is the verified category.
- A typical output flags 0 or 1 types. 3+ flags should be RARE.
- False positives are worse than false negatives.
  When in doubt, mark 0.

HALLUCINATION TAXONOMY (strict criteria):

H1 SCENE FABRICATION: Flag ONLY if the model describes a specific
WRONG setting that contradicts the ground truth.

H2 CRIME MISCLASSIFICATION: Flag ONLY if the model explicitly
identifies a DIFFERENT crime type than the verified one.

H3 CRIME OMISSION: Flag ONLY if the model explicitly states the
scene is normal/non-criminal AND the ground truth clearly
describes a crime.

H4 SEVERITY MINIMIZATION: Flag ONLY if the model accurately
describes events but uses language that explicitly downplays
criminal severity.

H5 ENTITY FABRICATION: Flag ONLY if the model mentions SPECIFIC
objects/features clearly NOT in the ground truth.

H6 PHANTOM ACTORS: Flag ONLY if the model mentions SPECIFIC
people/groups NOT in the ground truth.

Respond with ONLY a valid JSON object, no markdown:
{"H1": 0 or 1, "H2": 0 or 1, "H3": 0 or 1, "H4": 0 or 1,
 "H5": 0 or 1, "H6": 0 or 1, "confidence": "high|medium|low",
 "reasoning": "1-2 sentences citing specific evidence"}
```

---

## B. Forensic Annotation Rubric

Expert annotations in the UCA dataset [yuan2024surveillance] were supplemented with a forensic analysis rubric designed for court-admissible video evidence documentation [abdulrahaman2025ucacrime]. The rubric operationalizes ten evaluation criteria, each mapped to a specific legal admissibility concern under U.S. Federal Rules of Evidence and the Daubert standard [daubert1993]. Annotators recorded observable facts — visible actions, actors, objects, temporal sequences, environmental context — rather than inferring intent or causation. Deviations from rubric-structured annotations constitute measurable fabrication (H1, H5, H6), omission (H3), or distortion (H2, H4). The table below summarizes the criteria.

**Table B.1. Forensic annotation rubric with court-admissibility alignment.**

| Criterion | Court Admissibility Concern | Key Refs. |
|---|---|---|
| Crime Classification & Intent Detection | Relevance and elements of charged offense | [fre401] |
| Temporal Forensic Reconstruction | Timeline authentication and sequence documentation | [fre901], [swgde2024] |
| Subject Identification & Behavioral Analysis | Identification procedures and expert testimony | [daubert1993], [fre702] |
| Physical Evidence Documentation | Authentication and chain-of-custody | [fre901] |
| Violence & Weapon Analysis | Aggravating factors and degree of force | — |
| Criminal Network & Coordination Analysis | Conspiracy or joint enterprise elements | — |
| Modus Operandi Documentation | Prior bad acts evidence exceptions | — |
| Scene Analysis & Environmental Context | Foundation for scene reconstruction testimony | [fre401] |
| Escape Route & Exit Strategy Analysis | Premeditation and consciousness of guilt | — |
| Forensic Narrative & Court Readiness | Expert testimony standards for admissibility | [daubert1993], [fre702] |

---

## C. Code and Data Availability

All code, expert labels, prompt templates, and the cell-level result corpus are publicly released at:

https://github.com/opeyemiTaiwo/Prompting-Strategies-Reshape-Hallucination-Profiles

The repository contains:

- `llm_judge_labels.csv` — 456 pilot experiments with majority-vote H1–H6 labels
- `panel_raw_judge_labels.csv` — 893 raw per-judge pilot scores
- `human_spotcheck_50.csv` and `human_panel_agreement.json` — human validation data
- `Final_Hallucination_Analysis.ipynb` — full evaluation pipeline
- `Word_count.ipynb` and `human_spotcheck_scoring.ipynb` — supporting analyses
- `requirements.txt` — dependencies (Python 3.12, scikit-learn 1.5.x, sentence-transformers 2.x, anthropic 0.49.x, openai 1.x, google-generativeai 0.8.x)

Full-study artifacts (19,361 forensic reports, judge verdicts, human labels) are available upon request for the camera-ready version. Video data: UCF-Crime [sultani2018real], [ucfcrime_project]; annotations: UCA [yuan2024surveillance]; pre-extracted frames: [abdulrahaman2025ucacrime].

---

*Note: Bracketed tags such as [daubert1993] are citation keys carried over from the original LaTeX `\cite{...}` commands; resolve them against your bibliography when rendering the final reference list.*
