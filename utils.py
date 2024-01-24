# create a class to store the properties of each node, then create functions that will calculate each property
class Node:
    def __init__(self, settlement, angular_displacement, equilibrium_equation, node_reaction):
        self.settlement = settlement
        self.angular_displacement = angular_displacement
        self.equilibrium_equation = equilibrium_equation
        self.node_reaction = node_reaction



# create a class to store the properties of each span, then create functions that will calculate each property
class Span:
    def __init__(self, left_fem, right_fem, span_length, load, loading_condition, cord_rotation, left_moment,
                 right_moment, left_slope_deflection_equation, right_slope_deflection_equation,
                 reaction_at_left_node_on_span, reaction_at_right_node_on_span, span_a_value):
        self.left_fem = left_fem
        self.right_fem = right_fem
        self.span_length = span_length
        self.load = load
        self.loading_condition = loading_condition
        self.cord_rotation = cord_rotation
        self.left_moment = left_moment
        self.right_moment = right_moment
        self.left_slope_deflection_equation = left_slope_deflection_equation
        self.right_slope_deflection_equation = right_slope_deflection_equation
        self.reaction_at_left_node_on_span = reaction_at_left_node_on_span
        self.reaction_at_right_node_on_span = reaction_at_right_node_on_span
        self.span_a_value = span_a_value
