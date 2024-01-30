# Documentation for `calculate_beam_properties` Function

## Overview
The `calculate_beam_properties` function is a comprehensive tool designed for the structural analysis of beams in various configurations, including continuous beams with multiple spans, beams with cantilevers, and even frames. It evaluates shear forces, bending moments, reactions at supports, and accommodates settlement effects. This function is particularly useful in the field of civil and structural engineering for analyzing complex beam systems under various loading conditions.

## Function Signature
```python
def calculate_beam_properties(number_of_supports, number_of_internal_joints, span_data, settlement_positions, settlement_values, settlement_on_beam, first_node_fixed, last_node_fixed):
```

## Parameters
- `number_of_supports` (int): The total number of supports for the beam.
- `number_of_internal_joints` (int): The number of internal joints in the beam system.
- `span_data` (list of dictionaries): A list containing dictionaries for each span with keys for span length, load, loading condition, and other span-specific parameters.
- `settlement_positions` (list of ints): The positions of nodes along the beam where settlement occurs.
- `settlement_values` (list of floats): The settlement values corresponding to the positions in `settlement_positions`.
- `settlement_on_beam` (str): A flag indicating if there is settlement on the beam (`"yes"` or `"no"`).
- `first_node_fixed` (str): Indicates if the first node of the beam is fixed (`"yes"` or `"no"`).
- `last_node_fixed` (str): Indicates if the last node of the beam is fixed (`"yes"` or `"no"`).

## Returns
A dictionary containing:
- `shear_forces`: A list of shear forces calculated along the beam.
- `position_along_beam`: The positions along the beam corresponding to the calculated shear forces.
- `equation`: A list of slope deflection and equilibrium equations used in the analysis.
- `equationSolution`: The solutions to the system of equations.
- `listOfMoments`: A list of moments at various points along the beam.

## Example Usage
### Problem Statement
Consider a beam with 2 supports and 3 internal joints, making a total of 4 spans. The beam is subjected to various loading conditions including point loads, uniformly distributed loads, and no load on certain spans. Additionally, there is settlement at specific nodes of the beam. Calculate the shear forces, bending moments, and reactions at the supports.

### Sample Input
```python
number_of_supports = 2
number_of_internal_joints = 3
span_data = [
    {"span_length": 5, "load": 10, "loading_condition": "UDL"},
    {"span_length": 6, "load": 15, "loading_condition": "P_C"},
    {"span_length": 4, "load": 12, "loading_condition": "P_X", "span_a_value": 2},
    {"span_length": 7, "load": 8, "loading_condition": "UDL/2_R"}
]
settlement_positions = [1, 2]
settlement_values = [0.5, -0.3]
settlement_on_beam = "yes"
first_node_fixed = "no"
last_node_fixed = "no"
```

### Function Call
```python
results = calculate_beam_properties(number_of_supports, number_of_internal_joints, span_data, settlement_positions, settlement_values, settlement_on_beam, first_node_fixed, last_node_fixed)
```

## Further Development
- Enhance the function to handle cantilevers and frames.
- Introduce capability to analyze beams and frames with point moments.
- Incorporate a graphical representation for shear forces and bending moment diagrams.

---

This documentation provides a basic guide to utilizing the `calculate_beam_properties` function. It should be adapted and expanded based on the specific requirements and complexities of the structural systems being analyzed.