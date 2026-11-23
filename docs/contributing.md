# How to contribute to BERVO

Please open an issue in the BERVO GitHub repository with any suggestions for changes or updates.

## Method-agnostic variables

BERVO variables are **method-agnostic unless stated otherwise** ([issue #78](https://github.com/bioepic-data/bervo/issues/78)). A variable term names the physical, chemical, or biological quantity itself — not how a value was obtained. For example, *Air temperature* (`BERVO:0001370`) refers to the same variable whether it is a model parameter, a direct observation from a thermometer, or a value in a lab notebook with no context about how it was obtained; likewise, both CHESS's `L_2200` optical-analyser column and EcoSIM's `tlai_day_pft` output map to *Canopy leaf area index* (`BERVO:0001879`).

Whether a value was observed, calculated, or modelled belongs in dataset metadata (for example, ODM2 `MethodTypeCV` or ESS-DIVE method fields) rather than as separate observed/modelled variable pairs. BERVO models methods as concepts under *Method* (`BERVO:8000303`) for datasets to reference without restricting variables.

