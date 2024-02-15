  # the parameters needed for the FEM calculation are gotten from user
  # the fixed end moments are calculated based on the loading conditions
  # print("Key words for loading condition:"
  #       "\nNo loading on span (none)"
  #       "\nPoint load at center (P_C)"
  #       "\nPoint load at distance 'a' from left end and 'b' from the right end (P_X)"
  #       "\nTwo equal point loads, spaced at 1/3 of the total length from each other (P_C_2)"
  #       "\nThree equal point loads, spaced at 1/4 of the total length from each other (P_C_3)"
  #       "\nUniformly distributed load over the whole length (UDL)"
  #       "\nUniformly distributed load over half of the span on the right side (UDL/2_R)"
  #       "\nUniformly distributed load over half of the span on the left side (UDL/2_L)"
  #       "\nVariably distributed load, with highest point on the right end (VDL_R)"
  #       "\nVariably distributed load, with highest point on the left end (VDL_L)"
  #       "\nVariably distributed load, with highest point at the center (VDL_C)")
def calculate_left_and_right_fem(beam_spans, number_of_spans):
    length_of_beam = 0
    for i in range(number_of_spans):
        # Add the length of the current span to the total length of the beam
        length_of_beam += beam_spans[i].span_length

        # Check the loading condition of the current span and calculate the fixed end moments accordingly
        if beam_spans[i].loading_condition == 'P_C':
            # Point load at center: Calculate FEMs for a point load at the center of the span
            beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length) / 8
            beam_spans[i].left_fem = -1 * beam_spans[i].right_fem
        
        elif beam_spans[i].loading_condition == 'P_X':
            # Two equal point loads, each spaced at 1/3 of the span from the ends: Calculate FEMs for this condition
            a = beam_spans[i].span_a_value
            b = beam_spans[i].span_length - a
            beam_spans[i].right_fem = (beam_spans[i].load * b * a * a) / (beam_spans[i].span_length *
                                                                            beam_spans[i].span_length)

            beam_spans[i].left_fem = (beam_spans[i].load * b * b * a) / (beam_spans[i].span_length *
                                                                        beam_spans[i].span_length)
        
        elif beam_spans[i].loading_condition == 'P_C_2':
            # Two equal point loads, each placed at the center: Calculate FEMs for this condition
            beam_spans[i].right_fem = (2 * beam_spans[i].load * beam_spans[i].span_length) / 9
            beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

        elif beam_spans[i].loading_condition == 'P_C_3':
            # Three equal point loads, spaced at 1/4 of the total length from each other: Calculate FEMs for this condition
            beam_spans[i].right_fem = (15 * beam_spans[i].load * beam_spans[i].span_length) / 48
            beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

        elif beam_spans[i].loading_condition == 'UDL':
            # Uniformly distributed load over the entire span: Calculate FEMs for this condition
            beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 12
            beam_spans[i].left_fem = -1 * beam_spans[i].right_fem
        
        elif beam_spans[i].loading_condition == 'UDL/2_R':
            # Uniformly distributed load over the right half of the span: Calculate FEMs for this condition
            beam_spans[i].right_fem = (11 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[
                i].span_length) / 192
            beam_spans[i].left_fem = -1 * (5 * beam_spans[i].load * beam_spans[i].span_length *
                                            beam_spans[i].span_length) / 192
        
        elif beam_spans[i].loading_condition == 'UDL/2_L':
            # Uniformly distributed load over the left half of the span: Calculate FEMs for this condition
            beam_spans[i].right_fem = (5 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 192
            beam_spans[i].left_fem = -1 * (11 * beam_spans[i].load * beam_spans[i].span_length *
                                            beam_spans[i].span_length) / 192
        
        elif beam_spans[i].loading_condition == 'VDL_R':
            # Variably distributed load, maximum at the right end: Calculate FEMs for this condition
            beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 20
            beam_spans[i].left_fem = -1 * (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 30
        
        elif beam_spans[i].loading_condition == 'VDL_L':
            # Variably distributed load, maximum at the left end: Calculate FEMs for this condition
            beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 30
            beam_spans[i].left_fem = -1 * (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 20

        elif beam_spans[i].loading_condition == 'VDL_C':
            # Variably distributed load, maximum at the center: Calculate FEMs for this condition
            beam_spans[i].right_fem = (5 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 96
            beam_spans[i].left_fem = -1 * beam_spans[i].right_fem

        elif beam_spans[i].loading_condition == "none":
            # No loading on this span, set FEMs to 0
            beam_spans[i].right_fem = 0
            beam_spans[i].left_fem = 0
            print(f"No loading on span {i+1}")
    
    # Returning the total length of the beam and the beam_spans list with updated FEMs
    return length_of_beam, beam_spans
