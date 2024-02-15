from sympy import symbols, Eq, solve

EI = 1
def create_moments_symbols_from_sympy(number_of_spans, beam_spans):
    """
    Create symbolic variables representing the moments at the left and right ends of each span in the structure.

    Args:
    - number_of_spans: The total number of spans in the structure.
    - beam_spans: A list of Span objects representing each span in the structure.

    Returns:
    - beam_spans: Updated list of Span objects with left and right moments assigned.
    - list_of_end_moments: A list containing the symbolic variables representing the moments at the ends of each span.
    """
    list_of_end_moments = []  # Initialize an empty list to store the symbolic moments
    left_end = "a"  # Initialize the left end marker
    right_end = "b"  # Initialize the right end marker
    
    # Loop through each span in the structure
    for i in range(number_of_spans):
        # Create symbolic variables for the left and right moments of the current span
        beam_spans[i].left_moment, beam_spans[i].right_moment = symbols(f"M{left_end}{right_end} M{right_end}{left_end}")
        
        # Update the markers for the next span
        left_end = chr(ord(left_end) + 1)
        right_end = chr(ord(right_end) + 1)
        
        # Append the symbolic moments to the list
        list_of_end_moments.append(beam_spans[i].left_moment)
        list_of_end_moments.append(beam_spans[i].right_moment)
        
    # Return the updated list of spans and the list of symbolic moments
    return beam_spans, list_of_end_moments
  
  
def express_slope_deflection_equations_into_a_list(beam_spans, beam_nodes, number_of_spans, first_node_fixed, last_node_fixed):
    list_of_slope_deflection_equations = []
    for i in range(number_of_spans):
        if i == 0 and first_node_fixed == "no":
            beam_spans[i].left_slope_deflection_equation = Eq(0, EI * beam_spans[i].left_moment)
            beam_spans[i].right_slope_deflection_equation = Eq(
                (((3 * (beam_nodes[i + 1].angular_displacement - beam_spans[i].cord_rotation)) / beam_spans[i].span_length)
                + beam_spans[i].right_fem), EI * beam_spans[i].right_moment
            )

        elif i == number_of_spans - 1 and last_node_fixed == "no":
            beam_spans[i].left_slope_deflection_equation = Eq(
                (((3 * (beam_nodes[i].angular_displacement - beam_spans[i].cord_rotation)) / beam_spans[i].span_length)
                + beam_spans[i].left_fem), EI * beam_spans[i].left_moment
            )
            beam_spans[i].right_slope_deflection_equation = Eq(0, EI * beam_spans[i].right_moment)

        else:
            beam_spans[i].left_slope_deflection_equation = Eq(
                (((2 * ((2 * beam_nodes[i].angular_displacement) + beam_nodes[i + 1].angular_displacement - (
                    3 * beam_spans[i].cord_rotation))) / beam_spans[i].span_length) + beam_spans[i].left_fem),
                EI * beam_spans[i].left_moment
            )
            beam_spans[i].right_slope_deflection_equation = Eq(
                (((2 * ((2 * beam_nodes[i + 1].angular_displacement) + beam_nodes[i].angular_displacement - (
                    3 * beam_spans[i].cord_rotation))) / beam_spans[i].span_length) + beam_spans[i].right_fem),
                EI * beam_spans[i].right_moment
            )

        list_of_slope_deflection_equations.append(beam_spans[i].left_slope_deflection_equation)
        list_of_slope_deflection_equations.append(beam_spans[i].right_slope_deflection_equation)

    return beam_nodes, beam_spans, list_of_slope_deflection_equations


def express_list_of_equilibrium_equation(number_of_nodes, beam_nodes, beam_spans):
  list_of_equilibrium_equations = []
  for i in range(number_of_nodes):
      if i != 0 and i != number_of_nodes - 1:
          beam_nodes[i].equilibrium_equation = Eq(beam_spans[i - 1].right_moment + beam_spans[i].left_moment, 0)
      else:
          beam_nodes[i].equilibrium_equation = 0

      list_of_equilibrium_equations.append(beam_nodes[i].equilibrium_equation)
  return list_of_equilibrium_equations, beam_spans, beam_nodes