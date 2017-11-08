from domain import SimpleDomain
from sets import MutableFuzzySet, CalculatedFuzzySet
from operations import zadeh_not

distance_domain = SimpleDomain(0, 701)  # it is enough for distance domain to have 700 pixels
velocity_domain = SimpleDomain(20, 51)
direction_domain = SimpleDomain(0, 2)
acceleration_domain = SimpleDomain(-10, 11)
angle_domain = SimpleDomain(-90, 91)

correct_direction = MutableFuzzySet(direction_domain)
correct_direction.set_value_at(0, 0)
correct_direction.set_value_at(1, 1)

dangerously_close = CalculatedFuzzySet(distance_domain)
dangerously_close.set_calculated_memberships("l", alpha=0.1, beta=0.2)

close = CalculatedFuzzySet(distance_domain)
close.set_calculated_memberships("l", alpha=0.1, beta=0.35)

not_close = zadeh_not(close)
not_dangerously_close = zadeh_not(dangerously_close)

small_velocity = CalculatedFuzzySet(velocity_domain)
small_velocity.set_calculated_memberships("l", alpha=0.2, beta=0.3)

large_velocity = CalculatedFuzzySet(velocity_domain)
large_velocity.set_calculated_memberships("gamma", alpha=0.68, beta=0.7)

large_acceleration = CalculatedFuzzySet(acceleration_domain)
large_acceleration.set_calculated_memberships("gamma", alpha=0.68, beta=0.7)

sharp_right = CalculatedFuzzySet(angle_domain)
sharp_right.set_calculated_memberships("l", alpha=0.2, beta=0.4)

sharp_left = CalculatedFuzzySet(angle_domain)
sharp_left.set_calculated_memberships("gamma", alpha=0.6, beta=0.8)


