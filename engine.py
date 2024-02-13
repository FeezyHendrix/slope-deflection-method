from sympy import symbols, Eq, solve
from utils import Span, Node
from functions.fem import calculate_left_and_right_fem
from functions.slope_deflection_equation import create_moments_symbols_from_sympy, express_slope_deflection_equations_into_a_list, express_list_of_equilibrium_equation


def calculate_beam_properties(number_of_supports, number_of_internal_joints, span_data, settlement_positions, settlement_values, settlement_on_beam, first_node_fixed, last_node_fixed):
  number_of_nodes = number_of_supports + number_of_internal_joints
  number_of_spans = number_of_nodes - 1

  beam_nodes = []
  beam_spans = []

  settlement_variable = 0
  angular_displacement_variable = 0
  equilibrium_equation_variable = ""
  node_reaction_variable = 0
  for i in range(number_of_nodes):
      beam_nodes.append("")
      beam_nodes[i] = Node(settlement_variable, angular_displacement_variable, equilibrium_equation_variable,
                          node_reaction_variable)

  # make all the unknown angular displacements sympy symbols, and store them in a list, first and last are always = 0
  # Initialize an empty list to store the unknown angular displacements of the beam nodes
  list_of_unknown_angular_displacements = []

  # Start with the first node named "A"
  first_node = "A"

    # Loop through each node in the beam
  for i in range(number_of_nodes):
        # For internal nodes (not the first or the last node),
        # assign a symbolic variable for the angular displacement
        if i != 0 and i != number_of_nodes - 1:
            beam_nodes[i].angular_displacement = symbols(f"Theta_{first_node}")
            # Add the symbolic variable to the list of unknown angular displacements
            list_of_unknown_angular_displacements.append(beam_nodes[i].angular_displacement)
        else:
            # For the first and last nodes, initially create a symbolic variable
            # but then set the angular displacement to 0, assuming these nodes are fixed or
            # another condition is applied that removes their degrees of freedom for rotation
            beam_nodes[i].angular_displacement = symbols(f"Theta_{first_node}")
            beam_nodes[i].angular_displacement = 0

        # Move to the next node by incrementing the character used for naming
        first_node = chr(ord(first_node) + 1)




  left_fem_variable = 1
  right_fem_variable = 1
  cord_rotation_variable = 1
  left_moment_variable = 1
  right_moment_variable = 1
  left_slope_deflection_equation_variable = ""
  right_slope_deflection_equation_variable = ""
  reaction_at_left_node_on_span_variable = 1
  reaction_at_right_node_on_span_variable = 1
  span_a_value_variable = 1

  for i in range(number_of_spans):
    # Append an empty placeholder to the beam_spans list to maintain the correct indexing
    beam_spans.append("")
    # Create a new Span object for each span in the beam with the initialized variables
    # and specific values from the span_data input, which includes the span length, load,
    # and loading condition for each span.
    beam_spans[i] = Span(left_fem_variable, right_fem_variable, span_data[i]['span_length'], span_data[i]['load'],
                          span_data[i]['loading_condition'], cord_rotation_variable, left_moment_variable,
                          right_moment_variable, left_slope_deflection_equation_variable,
                          right_slope_deflection_equation_variable, reaction_at_left_node_on_span_variable,
                          reaction_at_right_node_on_span_variable, span_a_value_variable)


  #Calculate left and right rem
  length_of_beam, beam_spans = calculate_left_and_right_fem(beam_spans, number_of_spans)
  
  
  # Make all the end span moments sympy symbols, and store them in a list of unknown end moments
  beam_spans, list_of_end_moments = create_moments_symbols_from_sympy(number_of_spans, beam_spans)



  # next is to get the value of the support settlements
  # settlement_on_beam = input("Is there any settlement on the beam (yes) or (no)? ")
  if settlement_on_beam != "yes":
        for node in beam_nodes:
            node.settlement = 0
  else:
        for i, node in enumerate(beam_nodes):
            if i in settlement_positions:
                node.settlement = settlement_values[settlement_positions.index(i)]
            else:
                node.settlement = 0

#   # next is to determine the value of the cord rotation for each span
  for i in range(number_of_spans):
      beam_spans[i].cord_rotation = (
              (beam_nodes[i + 1].settlement - beam_nodes[i].settlement) / beam_spans[i].span_length)

  # next is to express the two slope deflection equations for each span, and store them in a list
  beam_nodes, beam_spans, list_of_slope_deflection_equations = express_slope_deflection_equations_into_a_list(beam_spans, beam_nodes, number_of_spans, first_node_fixed, last_node_fixed)
   
  # next is to define the equilibrium equations, and store it in a list
  list_of_equilibrium_equations, beam_spans, beam_nodes = express_list_of_equilibrium_equation(number_of_nodes, beam_nodes, beam_spans)

  # store the equations and the unknowns in lists
  equations = list_of_slope_deflection_equations + list_of_equilibrium_equations
  unknowns = list_of_end_moments + list_of_unknown_angular_displacements

  # next is to solve all the equations for the unknown moments and angular displacement
  solution = solve(tuple(equations), tuple(unknowns))

  print(equations)
  print(solution)
  print(solution[beam_spans[0].left_moment])
  print(list_of_end_moments)

  # next is to get the reactions for each span node
  for i in range(number_of_spans):
      if beam_spans[i].loading_condition == "P_C":
          beam_spans[i].reaction_at_right_node_on_span = ((solution[beam_spans[i].left_moment] + solution[beam_spans[i].right_moment] + (
                  beam_spans[i].load * (beam_spans[i].span_length / 2))) / beam_spans[i].span_length)
          beam_spans[i].reaction_at_left_node_on_span = beam_spans[i].load - beam_spans[i].reaction_at_right_node_on_span

      elif beam_spans[i].loading_condition == "P_X":
          a = beam_spans[i].span_a_value
          beam_spans[i].reaction_at_right_node_on_span = (
                  (solution[beam_spans[i].left_moment] + solution[beam_spans[i].right_moment] + (beam_spans[i].load * a)) / beam_spans[
              i].span_length)
          beam_spans[i].reaction_at_left_node_on_span = beam_spans[i].load - beam_spans[i].reaction_at_right_node_on_span

      elif beam_spans[i].loading_condition == "P_C_2":
          beam_spans[i].reaction_at_right_node_on_span = ((solution[beam_spans[i].left_moment] + solution[beam_spans[i].right_moment] + (
                  beam_spans[i].load * ((2 * beam_spans[i].span_length) / 3)) + (beam_spans[i].load * (
                  beam_spans[i].span_length / 3))) / beam_spans[i].span_length)
          beam_spans[i].reaction_at_left_node_on_span = 2 * beam_spans[i].load - beam_spans[
              i].reaction_at_right_node_on_span

      elif beam_spans[i].loading_condition == "P_C_3":
          beam_spans[i].reaction_at_right_node_on_span = ((solution[beam_spans[i].left_moment] + solution[beam_spans[i].right_moment] + (
                  beam_spans[i].load * ((3 * beam_spans[i].span_length) / 4)) + (beam_spans[i].load *
                                                                                ((2 * beam_spans[
                                                                                    i].span_length) / 4)) + (
                                                                  beam_spans[i].load * (
                                                                  beam_spans[i].span_length / 4))) /
                                                          beam_spans[i].span_length)
          beam_spans[i].reaction_at_left_node_on_span = 3 * beam_spans[i].load - beam_spans[
              i].reaction_at_right_node_on_span

      elif beam_spans[i].loading_condition == "UDL":
          beam_spans[i].reaction_at_right_node_on_span = ((solution[beam_spans[i].left_moment] + solution[beam_spans[i].right_moment] + (
                  beam_spans[i].load * ((beam_spans[i].span_length * beam_spans[i].span_length) / 2))) / beam_spans[
                                                              i].span_length)
          beam_spans[i].reaction_at_left_node_on_span = (beam_spans[i].load * beam_spans[i].span_length) - beam_spans[
              i].reaction_at_right_node_on_span

      elif beam_spans[i].loading_condition == "UDL/2_R":
          beam_spans[i].reaction_at_right_node_on_span = ((solution[beam_spans[i].left_moment] + solution[beam_spans[i].right_moment] + (
                  beam_spans[i].load * ((3 * beam_spans[i].span_length * beam_spans[i].span_length) / 8))) /
                                                          beam_spans[i].span_length)
          beam_spans[i].reaction_at_left_node_on_span = ((beam_spans[i].load * beam_spans[i].span_length) / 2) - \
                                                        beam_spans[i].reaction_at_right_node_on_span

      elif beam_spans[i].loading_condition == "UDL/2_L":
          beam_spans[i].reaction_at_right_node_on_span = ((solution[beam_spans[i].left_moment] + solution[beam_spans[i].right_moment] + (
                  beam_spans[i].load * ((beam_spans[i].span_length * beam_spans[i].span_length) / 8))) / beam_spans[
                                                              i].span_length)
          beam_spans[i].reaction_at_left_node_on_span = ((beam_spans[i].load * beam_spans[i].span_length) / 2) - \
                                                        beam_spans[i].reaction_at_right_node_on_span

      elif beam_spans[i].loading_condition == "VDL_R":
          beam_spans[i].reaction_at_right_node_on_span = ((solution[beam_spans[i].left_moment] + solution[beam_spans[i].right_moment] + (
                  beam_spans[i].load * ((2 * beam_spans[i].span_length * beam_spans[i].span_length) / 6))) /
                                                          beam_spans[i].span_length)
          beam_spans[i].reaction_at_left_node_on_span = ((beam_spans[i].load * beam_spans[i].span_length) / 2) - \
                                                        beam_spans[i].reaction_at_right_node_on_span

      elif beam_spans[i].loading_condition == "VDL_L":
          beam_spans[i].reaction_at_right_node_on_span = ((solution[beam_spans[i].left_moment] + solution[beam_spans[i].right_moment] + (
                  beam_spans[i].load * ((beam_spans[i].span_length * beam_spans[i].span_length) / 6))) / beam_spans[
                                                              i].span_length)
          beam_spans[i].reaction_at_left_node_on_span = ((beam_spans[i].load * beam_spans[i].span_length) / 2) - \
                                                        beam_spans[i].reaction_at_right_node_on_span
  '''
  for i in range(number_of_spans):
      print(beam_spans[i].reaction_at_right_node_on_span)
      print(beam_spans[i].reaction_at_left_node_on_span)
  '''

  # next is to get the reaction for each beam node
  for i in range(number_of_nodes):
      if i == 0:
          beam_nodes[i].node_reaction = beam_spans[i].reaction_at_left_node_on_span

      elif i == number_of_nodes - 1:
          beam_nodes[i].node_reaction = beam_spans[i-1].reaction_at_right_node_on_span

      else:
          beam_nodes[i].node_reaction = beam_spans[i-1].reaction_at_right_node_on_span +\
                                        beam_spans[i].reaction_at_left_node_on_span

  '''
  for i in range(number_of_nodes):
      print(beam_nodes[i].node_reaction)
  '''

  # next is to calculate the shear-forces on the beam and put into an array of shear-forces
  # also put the locations where there are loads into a separate array, for the plotting of the shear force diagram
  # the end reactions for each span are also calculated
  position_along_beam = [0]
  shear_forces = [0]
  sf = 0
  for i in range(number_of_spans):
      x = 0
      sf += beam_nodes[i].node_reaction
      position_along_beam.append(x)
      shear_forces.append(sf)
      if beam_spans[i].loading_condition == "P_C":
          x = beam_spans[i].span_length/2
          while i != 0:
              x += beam_spans[i-1].span_length
              i -= 1
          sf -= beam_spans[i].load

          position_along_beam.append(x)
          shear_forces.append(sf)

      elif beam_spans[i].loading_condition == "P_X":
          a = beam_spans[i].span_a_value
          x = beam_spans[i].span_length - a
          while i != 0:
              x += beam_spans[i-1].span_length
              i -= 1
          sf -= beam_spans[i].load

          position_along_beam.append(x)
          shear_forces.append(sf)

      elif beam_spans[i].loading_condition == "P_C_2":
          x = beam_spans[i].span_length - beam_spans[i].span_length/3
          while i != 0:
              x += beam_spans[i-1].span_length
              i -= 1
          sf -= beam_spans[i].load
          position_along_beam.append(x)
          shear_forces.append(sf)

          x = beam_spans[i].span_length - (2*beam_spans[i].span_length)/3
          while i != 0:
              x += beam_spans[i-1].span_length
              i -= 1
          sf -= beam_spans[i].load
          position_along_beam.append(x)
          shear_forces.append(sf)

      elif beam_spans[i].loading_condition == "P_C_3":
          x = beam_spans[i].span_length - beam_spans[i].span_length / 4
          while i != 0:
              x += beam_spans[i - 1].span_length
              i -= 1
          sf -= beam_spans[i].load
          position_along_beam.append(x)
          shear_forces.append(sf)

          x = beam_spans[i].span_length - (2 * beam_spans[i].span_length) / 4
          while i != 0:
              x += beam_spans[i - 1].span_length
              i -= 1
          sf -= beam_spans[i].load
          position_along_beam.append(x)
          shear_forces.append(sf)

          x = beam_spans[i].span_length - (3 * beam_spans[i].span_length) / 4
          while i != 0:
              x += beam_spans[i - 1].span_length
              i -= 1
          sf -= beam_spans[i].load
          position_along_beam.append(x)
          shear_forces.append(sf)

      elif beam_spans[i].loading_condition == "UDL":
          while i != 0:
              x += beam_spans[i - 1].span_length
              i -= 1

          for u in range(beam_spans[i].span_length):
              x += u
              sf -= beam_spans[i].load * u
              position_along_beam.append(x)
              shear_forces.append(sf)

      elif beam_spans[i].loading_condition == "UDL/2_R":
          x = beam_spans[i].span_length/2
          while i != 0:
              x += beam_spans[i - 1].span_length
              i -= 1

          for u in range(beam_spans[i].span_length):
              x += u
              sf -= beam_spans[i].load * u
              position_along_beam.append(x)
              shear_forces.append(sf)

      elif beam_spans[i].loading_condition == "UDL/2_L":
          while i != 0:
              x += beam_spans[i - 1].span_length
              i -= 1

          for u in range(beam_spans[i].span_length/2):
              x += u
              sf -= beam_spans[i].load * u
              position_along_beam.append(x)
              shear_forces.append(sf)

      elif beam_spans[i].loading_condition == "VDL_R":
          while i != 0:
              x += beam_spans[i - 1].span_length
              i -= 1

          for u in range(beam_spans[i].span_length):
              x += u
              sf -= (beam_spans[i].load * u * u) / (2*beam_spans[i].span_length)
              position_along_beam.append(x)
              shear_forces.append(sf)

      elif beam_spans[i].loading_condition == "VDL_L":
          while i != 0:
              x += beam_spans[i - 1].span_length
              i -= 1

          for u in range(beam_spans[i].span_length):
              x += u
              sf -= ((beam_spans[i].load * u)/beam_spans[i].span_length) * (2 - (u/beam_spans[i].span_length))
              position_along_beam.append(x)
              shear_forces.append(sf)

      if i == number_of_spans - 1:
          position_along_beam.append(length_of_beam)
          sf += beam_nodes[i+1].node_reaction
          shear_forces.append(sf)

  serializable_solution = {str(key): str(val) for key, val in solution.items()}
  serializable_list_of_moments = [str(moment) for moment in list_of_end_moments]
  serializable_equations =[str(equation) for equation in equations]
  serializable_shear_force = [str(shear_force) for shear_force in shear_forces]
  return { "shear_forces": serializable_shear_force, "position_along_beam": position_along_beam, "equation": serializable_equations,  "equationSolution": serializable_solution, "listOfMoments": serializable_list_of_moments }

  # make code work with settlement
  # make code work for beams with cantilever
  # make code work for frames
  # make code work for beams and frames with point moment
