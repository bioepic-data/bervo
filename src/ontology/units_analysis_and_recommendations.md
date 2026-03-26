# BERVO has_units Column Analysis and Recommendations

## Summary
- **Total entries**: 2,320
- **Entries missing units**: 1,130 (48.7%)
- **Entries with units**: 1,190 (51.3%)

## Categories of Missing Units

### 1. Root Variable Class (1 entry)
- **BERVO:0000000** (Variable) - Should receive **`NA`** as this is the abstract root class

### 2. Parent/Abstract Category Classes (~18 entries)
These diffusivity parent classes should receive **`NA`**:
- BERVO:0001838 - Argon diffusivity
- BERVO:0001839 - Carbon dioxide diffusivity  
- BERVO:0001840 - Methane diffusivity
- BERVO:0001841 - Oxygen diffusivity
- BERVO:0001842 - Nitrogen diffusivity
- BERVO:0001843 - Nitrous oxide diffusivity
- BERVO:0001844 - Ammonia diffusivity
- BERVO:0001845 - Nitrate diffusivity
- BERVO:0001846 - Phosphate diffusivity

### 3. Equilibrium Constants (~24 entries)
These need units extracted from their definitions and added to Column 13.
Examples of units to extract:
- `mol^2 m^-6`
- `mol m^-3`
- `mol^3 m^-9`
- `m^3 mol^-1`
- etc.

### 4. Dimensionless Parameters (fractions, ratios) (~50+ entries)
These should receive **`NONE`**:
- Fractions (e.g., "Minimum fraction of growth allocated to leaf")
- Ratios (e.g., "Minimum N:C,P:C in leaves relative to max values")
- Shape parameters
- Partition parameters
- Allocation parameters

### 5. Variables with Physical Dimensions (~900+ entries)
These need appropriate units based on their measurement type:

#### Common unit patterns found in similar entries:
- **Flux variables**: `g d-2 h-1`, `MJ d-2 h-1`, `mol d-2`
- **Mass/Content variables**: `g d-2`, `Mg d-2`
- **Volume variables**: `m3 d-2`
- **Concentration variables**: `g m-3`, `mol m-3`
- **Rate constants**: `h-1`, `h^-1`
- **Diffusivity**: `m2 h-1`
- **Solubility coefficients**: `g solute /g gas`
- **Length**: `m`
- **Pressure**: `MPa`
- **Temperature**: `C` or `K`

### 6. Special Cases

#### Grid/Index Variables
Variables like "Soil surface layer number" should receive **`NONE`** (count/index)

#### Flag/Category Variables  
Variables like "Fertilizer release type" should receive **`NA`** (categorical)

## Recommended Approach

Given the scale (1,130 entries), I recommend a semi-automated approach:

1. **Manual fixes for clear cases** (~100 entries):
   - Root Variable class: NA
   - Parent diffusivity classes: NA  
   - Dimensionless fractions/ratios: NONE
   - Categorical/flag variables: NA

2. **Pattern-based extraction** (~50 entries):
   - Equilibrium constants: extract units from definitions

3. **Category-based inference** (~900+ entries):
   - Use category + label patterns to infer units
   - Climate force variables with "temperature" → C
   - Variables with "concentration" → g m-3 or mol m-3
   - Variables with "flux" → appropriate flux units based on substance
   - Variables with "content" or "mass" → g d-2 or similar

4. **Manual review**:
   - Review all automated assignments
   - Check consistency within categories
   - Verify units match definitions

## Next Steps

Would you like me to:
1. Create a comprehensive Python script to automate the majority of these changes?
2. Start with manual edits for specific categories (e.g., just equilibrium constants)?
3. Focus on a particular subset (e.g., all Climate force variables)?

The task is manageable but requires systematic handling given its scale.
