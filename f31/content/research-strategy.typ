#import "/template/components.typ": *
= Research Strategy

== Overall Approach

In Aim 1, we are going to put together a Graph Neural Network trained on an ERK2 Gaussian network model as well as on NMR and HDX-MS data to predict the functional motion of ERK2 kinase, and then we are going to check if that same model can accurately predict the conformational change of other kinases of varying degrees of similarity to ERK2. In Aim 2, we are going to investigate if different kinases have similar mutation to nonfunction thresholds by transfecting HEK293 cells with varying, increasingly damaged, kinase production genes in a controlled fashion, and then checking downstream phosphorylation as a measure of kinase function with western blotting.

Aim 1 lets us investigate whether or not protein conformational change can be predicted across a family of proteins with similar functions, however, failing to account for misfolding tolerance may lead to statistical bias. Aim 2 will independently provide us with a quantifiable threshold metric for acceptable structural damage that can be used to augment the GNN's training data and/or process. This tolerance threshold is valuable as a free and open-source resource to the scientific computing community even in the event that Aim 1 fails.

#figure(
  image("../../build/figures/gnm_comparison.svg", width: 90%),
  caption: [GNM fluctuation profiles of the four kinases under investigation, with ERK2 serving as the anchor protein for the KING model.]
)

#figure(
  image("../../build/figures/aim1_pipeline.svg", width: 90%),
  caption: [Aim 1 data flow: structural and dynamics data from public repositories and empirical sources feed into the KING graph neural network, which is then evaluated on novel kinases.]
)

// HEY NICK — your original brackets called for "Display Images of the HEK293 cells and a gradient of sample photographs showing a decrease in phosphorylation."
// We don't have those photos and they aren't in our database. You can either commission/find them later, or just delete this comment and skip the figure.

#figure(
  image("../../build/figures/aim1_correlation.svg", width: 95%),
  caption: [Anticipated positive result for Aim 1: a row of correlation plots per kinase comparing empirically measured NMR (top) and HDX-MS (bottom) values against KING's predictions.]
)

#figure(
  image("../../build/figures/aim2_mutation_curve.svg", width: 80%),
  caption: [Anticipated positive result for Aim 2: phosphorylation signal intensity as a function of mutation load. The hypothesis is supported if all four kinases show similar threshold behavior.]
)

== Preliminary Studies

My first preliminary study would be successfully recreating HDX-MS and NMR Spectroscopy on ERK2. This will need to be validated against public processed data, and I would display correlation curves here. This can serve as a backbone for my next preliminary study, as well as for future GNN training.

My second preliminary study is a proof-of-concept GNN that is trained to predict NMR relaxation measurements/orders from HDX-MS data. I include a correlation plot to represent how close the estimates were to the empirically found values. This shows that not only is my group capable of handling HDX-MS and NMR, we've already made a GNN before, and our GNN can be used to predict protein conformational data. This will again need correlation plots to demonstrate how close the GNN came to the empirically recorded value.

#figure(
  image("../../build/figures/preliminary_studies.svg", width: 95%),
  caption: [Preliminary studies validation: (a) in-house HDX-MS recreation correlated with published reference values, and (b) proof-of-concept GNN predicting NMR S² order parameters from HDX-MS uptake data.]
)

== Aim 1: Flexibility Characterization of the Kinase Protein Family

In order to properly begin designing custom proteins, we need to improve our ability to predict what active conformational functionality looks like. This aim seeks to take a simple, well documented, generally understood protein that performs an action in motion, and to computationally isolate the conformational properties that allow and support this behavior. ERK2 has exceptionally well discussed L↔R conformational changes, which makes it an ideal origin point for this experiment. I hypothesize that a Graph Neural Network (GNN) of protein activity derived from ERK2 will demonstrate transferability across the broader kinase family.

=== Overview of Experimental Design

Publicly available ERK2 NMR, HDX-MS, smFRET and GNM data will be acquired from PRIDE, PDC, and iGNM 2.0. This data will be tabulated along with empirical NMR and HDX-MS data from preliminary trials. This data will be then used to train the GNN. Lastly, the dynamic behavior of other kinases will be approximated by the GNN, and those approximations will be compared to the NMR order parameters and the HDX uptake data for the 3 new kinases.

=== Aim 1A: Development of the KINase Graphical neural network (KING)

*Experimental Design:* For the development and training of KING I plan to use GROMACS and PyTorch. Amino acid residues will represent individual nodes with physical proximity determining their boundaries. Each node will encode for its position, its chemical properties, and GNM derived fluctuation values. However, KING will function much in the same way a transformer GNN does; all nodes will interact with each other, and the message-passing function will be based on position with respect to GNM parameters. This includes both experimentally gathered and public-processed data. Training data for KING will consist of three independent microsecond molecular dynamics simulation replicates of ERK2, with each replicate providing a frame at every 20 picoseconds returning 50,000 frames per replicate. The GNN will then be provided with a new, freshly generated ERK2 gaussian network model graph from our collaborator at the University of Florida, which we will use to validate the model's blind efficacy.

*Anticipated Results and Alternatives:* I expect the prediction produced by KING to be accurate to a Pearson Correlation > 0.75. It is possible that KING becomes overfitted to ERK2, in which case we will need to allocate time for improving cross-validation in training, increase the sampling length, and retrain the model using dropout regularization. In the case of delays in Aim 2, further time can be allotted to training the model.

=== Aim 1B: Evaluation of neighbor kinase family proteins

*Experimental Design:* We then experimentally generate GNM graphs of ABL1, PKA, and JNK3, and feed them to KING to approximate NMR, HDX and smFRET values for these kinases. We then will run quadruplicate HDX-MS, NMR, and smFRET experiments to record ground truth values for all 3. We will then evaluate KING's output by contrasting its prediction against the ground truth values we've experimentally discovered, with accuracy reported as the mean difference from the approximated value.

*Anticipated Results and Alternatives:* KING's predictions of ABL1, PKA, and JNK3 ideally will return a Pearson correlation > 0.7 and a Spearman correlation > 0.65. In the case that KING fits well to some of the kinases, but not all of them, that portion of the experiment can pivot into discussing the transferability of the model and its limitations in regards to that kinase.

*Summary of Aim 1:* The collective results of Aim 1 establish a method by which we can mathematically predict the motion in which a protein functions, and a way to investigate if that prediction can generalize within familial function constraints. They provide a basis by which we can generalize across kinases, however we're aware it's unlikely that KING would be able to properly predict the dynamics of a slightly damaged, albeit functioning kinase. However, mutation and damage causes conformational change and affects molecular dynamics. Aim 2 seeks to identify a quantifiable threshold at which that becomes statistically relevant to better inform KING's functionality.

== Aim 2: Analyzing the Significance of Mutations to Kinase Family Function

*Rationale and Hypothesis:* Aim 1 provides us with KING, with the purpose of predicting the dynamic profiles of kinase proteins. However in order for such a model to be clinically useful, it will need to be able to modify its final prediction by accounting for proteins that are structurally perturbed in some way, yet also able to mostly perform the same function as their standard counterparts. As such, our studies seek to discover a threshold of protein function loss, wherein accumulated point mutations cause kinases to cease to properly function.

*Hypothesis:* Across the kinase family there will be a comparably equivalent mutation load threshold where the protein ceases to function as intended.

=== Overview of Experimental Design

Starting with ERK2 and moving on to the ABL1, PKA, and JNK3 kinases, we will transfect their genes into HEK293 cells, and allow them to proliferate for 3 passages at 80% confluency to stabilize. We then perform a western blot analysis of the kinases, using densitometric pixel brightness intensity as a way to quantify phosphorylation, which is used as a metric for testing kinase function. This process will then be repeated, but each time with an increase in mutation load. We will use error-prone PCR to reliably produce experimental runs with increasing random point mutation load via modification of dNTP concentration and introduction of mutagenic dNTPs, continuing until 10% of final blot intensity is reached. The final publication will include graphs of average blot intensity (y-axis) vs. mutation load in number of point mutations (x-axis).

=== Aim 2A: Error-prone PCR and Transfection of Increasingly Damaged Kinase Genetics

*Experimental Design:* Using a low-fidelity variant of Taq DNA polymerase sourced from Thermo-Fisher Scientific, a predictable number of genetic mutations can be induced due to the variant's inability to proofread. This is achieved by modifying the initial concentration of dNTPs, as well as a systemic progressive addition (1 μg/mL step) of mutagenic dNTP analogues. These mutations are random but are shown to have a strictly linear relationship with random point mutations. Once DNA aggregates are prepared, T-Vector cloning is employed with linearized plasmids (sourced from Curia Biologics) to insert the PCR product into plasmid form. Cells are grown and prepared in complete media to 80% confluency prior to transfection. The day before transfection the cells are trypsinized, and plated into 12-well plates in 0.5 mL growth media composed of Opti-MEM I Reduced Serum Media, Gibco Dulbecco's Modified Eagle Medium (DMEM), 4 mM Gibco L-Glutamine, and 10% Gibco Fetal Bovine Serum (henceforth referred to as "Complete Media"). PCR Product DNA is diluted 0.5 μg DNA / 100 μL Opti-MEM I reduced serum media without serum, and is then incubated with 1.5 μL of Lipofectamine LTX Reagent (Thermo-Fisher Scientific) for 30 minutes, and then subsequently added to cell-containing wells, and incubated at 37°C at 5% CO₂. Baseline phosphorylation validation will be performed with serum-deprivation to reduce basal signaling activity by standard western blotting with phosphoro-antibodies.

*Anticipated Results & Alternatives:* HEK293 cells are known to be a relatively hardy and functional cell line, so difficulty in maintaining viability and successful transfection is not expected. If difficulties in obtaining supplies for transfection occur, Curia Biologics is also capable of providing HEK293 cell culture supplies in a similar price range. If validation fails during western blotting pre-trial, transfection can be outsourced to potential collaborators at the University of Florida.

=== Aim 2B: Quantifying Downstream Phosphorylation of Mutant/Damaged Kinases

*Experimental Design:* As transfection of kinase-related plasmids into HEK293 cells is completed, we can move directly into quantifying their ability to function. Similar to the validation test, cells are serum deprived to reduce the effects of basal signaling. Using Western blotting with phosphorylation antibodies, we can approximate kinase function. We will report kinase activity as a pixel-based blot intensity measurement. We will perform these experiments through each kinase variety, with increasing mutation load, until 10% (compared to original w/ zero errors) blot intensity is reached. This data will then be analyzed to establish a mutation threshold at the mutation load corresponding to the greatest derivative of phosphorylative intensity with respect to mutation load. Western blotting supplies to be purchased from Thermo-Fisher Scientific.

*Anticipated Results & Alternatives:* We expect the function curve to behave in an exponential manner with an R-squared value > 0.75. To confirm our hypothesis, we would need to compare the mutation load points corresponding to this maximal derivative for each kinase, and establish that they are meaningfully similar via independent sampling t-tests at α = 0.05. This experiment and measurement will be performed alongside Aim 1A, with minimal interconnectedness allowing for extremely low friction between aims.

#figure(
  image("../../build/figures/aim2_flowchart.svg", width: 95%),
  caption: [Aim 2 workflow: progression from wild-type kinase gene through error-prone PCR, transfection, culture, and western blot phosphorylation readout.]
)

*Summary of Aim 2:* The collective results of Aim 2 will allow us to establish a mathematical representation of how much conformational change a kinase can withstand before it has a statistically relevant chance of functional loss. This information is critically important to the training of KING, as it provides some context to the model's ability to interpret "less-than-perfect" proteins. This will provide us with a methodology for validating the protein conformations predicted by more advanced computational models by including these imperfections.

== Timeline and Rigor

=== Timeline

Concerning Aim 1, we expect 4–6 months for the prototyping and development of KING's code and framework. If cross-validation and dropout regularization are required, that can be performed independent of any other task. The evaluation of neighboring kinases is expected to take 8–16 months, and is the experiment with the most risk given the complexity of the tasks involved. It has been constructed so that some portions of it can be performed simultaneously with other sub-aims. Preliminary ground truth data can be acquired during the development of KING's framework, however the second half of the aim is dependent on successful development of the GNN. Aim 1 and Aim 2 can be performed simultaneously. Concerning Aim 2, we expect our error-prone PCR process to take 10–14 months. Progress within this aim has a rate-limiting step-wise relationship with the subsequent quantification of downstream phosphorylation, which will take likely 12–16 months. We would like to include an additional 12 months for the training of personnel on all requisite software and technology. If all proceeds perfectly, this project will take 30 months to complete. At most it will take 36 months, just around 3 years to fully complete.

#figure(
  image("../../build/figures/timeline.svg", width: 95%),
  caption: [Project timeline showing the parallel structure of Aim 1 and Aim 2 across the 30–36 month duration of the proposed work.]
)

=== Rigor

All experiments, validations, and baselines will be performed in quadruplicate with conditions randomized. Kinases will be assigned a letter at random (Kinase A, B, C, and D) by the laboratory principal investigator upon arrival. All researchers will be blinded to the identity of the kinase they are working on in any given experiment. The amount of mutation load during the Aim 2 trials will be randomized and assigned a non-identifiable experiment title (e.g., "Kinase B, Mutation trial #3"). A masterlist corroborating the trials to their true values will be kept encrypted in a university cloud server, with three backups on separate hard drives. Secure version control will be performed via GitHub with Mozilla SOPS, and physical backups will be updated monthly.

Western blots typically report a conservative coefficient of variation near 20%; if we consider a minimum biologically significant variation in blot intensity to be 50%, a power analysis indicates that with quadruplicate experiments given α = 0.05 and (1−β) = 0.80, we report a d-value of 2.5, indicating our quadruplicate experiments are sufficient to detect a signal difference with a power > 80%. HEK293 cells originate from an immortalized female cell line, and as such are all biologically female. We acknowledge that NIH SABV policy applies to human studies and any vertebrate animals, and as such sex is not a relevant variable for a commonplace immortalized cell line. During initial processing, all key biological resources will be validated with respect to their source. Cell lines will be checked via STR profiling, plasmid sequences will be confirmed via third-party nanopore sequencing, and antibody lots will be validated with western blots to confirm molecular weights. Once finished, all code and architecture, variable weights, training data, ground truth values, baselines, and source material will be compiled on GitHub under a GPL-3.0 license.

#bibliography("/f31/refs.bib", title: "References", style: "american-medical-association", full: true)
