# In-Silico Tuberculosis Granuloma Formation and Progression

This repository contains CompuCell3D (CC3D) based simulations modeling the formation and progression of tuberculosis granulomas. Specifically, these models investigate the fate of the granuloma based on the ontogenic origin of the macrophages involved in its formation and possible therapeutic interventions.

## Repository Structure

Each main directory in this repository represents a distinct simulation case. Inside each simulation folder, you will find:
* An **XML file** defining the model properties.
* **Two Python files** (`steppables.py` and the main simulation script) setting up and controlling different biological behaviors.
* (outside the simulation folder) A **`runcc3d.py` script** intended to be executed via the terminal to run replicates for that specific case.

---

## Simulation Scenarios

### `epivar_wo_mec`
**Epithelial Variation without Meclizine Treatment**  
Simulates the baseline granuloma composition variations without any drug interventions. 
* **Composition Variants:** Alveolar vs. Inflammatory proportions tested at 25%, 50%, and 75%.
* **Phenotype Variants:** Varying proportions of oxidized vs. reduced phenotypes in infected macrophages (0%, 50%, and 100% reduced, with complementary oxidized proportions). 

### `midepi_wo_inh`
**Mid-Epithelization (parameter) without Isoniazid (INH)**  
Simulates the baseline dynamics of granuloma progression based purely on structural cellular changes.
* **Parameter Tested:** Extent of macrophage epithelization adjusted via the surface parameter (15, 16.5, and 18).
* **Objective:** To observe the isolated effect of epithelization on the formation and structural progression of the granuloma.

### `No_killingTcell`
**Simulations with T cells without cytotoxic capacity**  
Simulates the T cell effectiveness in the simulation. 
* **Parameters Tested:** Cytotoxic capacity of T cells set to 0
* **Objective:** To evaluate the importance of T cells in elimiation of infected macrophagse and its effect on granuloma dynamics

### `midepi_w_inh`
**Mid-Epithelization (parameter) with Isoniazid (INH)**  
Simulates the physical barriers to drug efficacy.
* **Parameters Tested:** Extent of macrophage epithelization (surface parameters 15, 16.5, and 18) alongside a separate diffusion field for INH.
* **Objective:** To evaluate how the degree of cellular epithelization impacts the physical penetration and distribution of the INH drug within the granuloma.

### `epivar_w_mec`
**Epithelial Variation with Meclizine & INH Treatment**  
Simulates active, combination pharmacological intervention and its effect on structural composition.
* **Treatment Mechanism:** Simulates Meclizine treatment by switching the epithelial parameter at 10,000 Monte Carlo Steps (MCS), administered alongside INH.
* **Composition Variants:** Epithelial vs. Inflammatory proportions (25%, 50%, 75%).
* **Phenotype Variants:** Oxidized vs. Reduced phenotypes in infected macrophages (0%, 50%, 100% reduced).

---

## How to Run

To execute the simulations, navigate to the desired directory in your terminal and run the execution script. For example:

```bash
cd epivar_wo_mec
python runcc3d.py
