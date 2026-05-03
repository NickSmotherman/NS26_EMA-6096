#import "/template/components.typ": *
= Specific Aims

Along with the recent increase in development of machine-learning models, there have been successful forays into computationally designing custom proteins. Multiple international research groups have already managed to use ML methods to accurately predict and produce proteins that do not exist in nature. However, producing a protein complex that can reliably perform a function (enzymes, hormones, catalysts) has proven to be difficult. Presently, it is possible to easily identify the stable state of a protein, but most actionable proteins have excited states that such models are unable to accurately predict. Progression towards the goal of quantifiably useful custom proteins necessitates ML methods capable of identifying non-equilibrium protein states. Many existing models have an inherent "bias" that stems from authors focusing too much on a single protein or complex, leading to statistically impossible stability values inconsistent with nature. The source of that bias may be circumvented by using protein subfamilies and superfamilies, which can then be incorporated by existing models to account for their internal stability bias.

#goal[The long-term goal of this project is to develop a public Graph Neural model (GNN) that can accurately predict the ways in which activated proteins interact with their attached protein complexes, as well as the proteome at large. Furthermore, a clinically useful model must also account for tolerances to structural perturbation, identifying a threshold where significant structural deviation from normal flexibility results in a loss of function.]

#objective[The objective of this experiment is to develop and evaluate a transformer graph neural network (GNN) that might compensate for hidden bias in existing models, and to investigate the value of functional damaged proteins in GNN training data.]

#rationale[Kinases as a protein family are very well studied. ERK2 in particular, has exceptionally well discussed conformational changes and lots of publicly availible data, which makes it an ideal origin point for an experiment in familial generalization. Building on this, preliminary work in our lab has successfully recreated HDX-MS and NMR Spectroscopy on ERK2 (validated against public processed data) and built a proof-of-concept GNN that predicts NMR relaxation orders from HDX-MS data, establishing technical feasibility for the proposed expanded model.]

#central-hypothesis[
  A Graph Neural Network (GNN) of protein activity derived from ERK2 will demonstrate transferability across the broader kinase family, and across that family there will be a comparably equivalent mutation load threshold where the protein ceases to function as intended.
]

#aim(1, [Flexibility Characterization of the Kinase Protein Family],
  hypothesis: [
    A Graph Neural Network (GNN) of protein activity derived from ERK2 will demonstrate transferability across the broader kinase family.
  ],
  approach: [
    HDX-MS, Molecular dynamics simulation, NMR spectroscopy, and smFRET data on ERK2 will be used as a benchmark against an existing Gaussian Network Model (GNM) of ERK2. This validated GNM, along with Molecular dynamics simulation data will be used as training data for a GNN. This GNN will then be applied to the structurally diverse selection of kinases ABL1 (tyrosine kinase), PKA (serine/threonine kinase, AGC group), and JNK3 (MAPK group) for contrast. Validation will be performed by comparing predicted profiles against experimentally derived NMR order parameters and HDX-MS uptake data.
  ],
  outcomes: [
    I expect to see that across the broad family of kinases the relevant structural change to be similar and for the model to be an effective predictor, but individual factors must be investigated as well.
  ],
  pitfalls: [
    It is possible that the GNN becomes overfitted to ERK2, in which case we will need to allocate time for improving cross-validation in training, increase the sampling length, and retrain the model using dropout regularization.
  ],
)[]

#aim(2, [Analyzing the Significance of Mutations to Kinase Family Function],
  hypothesis: [
    Across the kinase family there will be a comparably equivalent mutation load threshold where the protein ceases to function as intended.
  ],
  approach: [
    HEK293 cells will be transfected with either standard functioning kinase or mutant kinase constructs. Mutant constructs will be generated using error-prone PCR to produce incrementally increasing mutation loads across ABL1, PKA, JNK3, and ERK2. Cells cultured in complete media will be serum-deprived to reduce basal signaling activity. Downstream phosphorylation will be checked with western blotting. Transfection experiments will be performed for increasingly mutated kinase constructs to identify the mutation load at which kinase function is lost across the family.
  ],
  outcomes: [
    Similarly, I expect there will be a common mutation threshold of protein damage linking to nonfunction.
  ],
  pitfalls: [
    If difficulties in obtaining transfection supplies occur, Curia Biologics — a commercial supplier — can provide HEK293 cell culture supplies in a similar price range. If validation fails during western blotting pre-trial, transfection can be outsourced to potential collaborators at the University of Florida.
  ],
)[]

#impact[
  The impact of this study has the potential to be a first step towards widespread innovation in many sectors. With an accurate GNN, it would become possible to reorient existing methods, leading to a boom in the medical field. Cellular delivery vectors, vaccines, treatments for autoimmune disorders, and custom anti-bodies are all possible novel breakthroughs.
]
