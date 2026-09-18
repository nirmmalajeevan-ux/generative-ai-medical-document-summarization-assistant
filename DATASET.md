# Dataset Information

## Recommended dataset: Microsoft Clinical Visit Note Summarization Corpus

Repository:
https://github.com/microsoft/clinical_visit_note_summarization_corpus

This public corpus contains **synthetic clinical encounters** and includes dialogue transcripts, clinical notes and associated metadata. It combines two collections:

- MTS-Dialog
- ACI-Bench

The publisher states that the corpus is intended for clinical note generation and summarization research and is distributed under **CC BY 4.0**.

The upstream repository was archived by Microsoft in June 2026, but remains publicly readable.

## Alternative dataset: MIMIC-III

PhysioNet:
https://physionet.org/content/mimiciii/1.4/

MIMIC-III contains de-identified clinical data and is widely used in medical NLP research. Access is controlled. Researchers must satisfy PhysioNet credentialing and data-use requirements before downloading restricted files.

For a classroom GitHub submission, the Microsoft synthetic corpus is easier to share because it avoids distributing restricted clinical data.

## Sample data in this repository

The file `data/sample_clinical_notes.csv` contains a few **original synthetic examples created only for demonstrating the application**. They are not copied from MIMIC or any real patient record.

## Citation / attribution

If you use the Microsoft corpus in experiments or a report, cite the dataset's upstream README and the associated publications listed there. Follow the dataset's CC BY 4.0 attribution requirements.
