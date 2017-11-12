from domain import SimpleDomain
from sets import MutableFuzzySet, CalculatedFuzzySet
from operations import zadeh_not

distance_domain = SimpleDomain(0, 1301)
velocity_domain = SimpleDomain(20, 51)
direction_domain = SimpleDomain(0, 2)
acceleration_domain = SimpleDomain(-10, 11)
angle_domain = SimpleDomain(-90, 91)

correct_direction = MutableFuzzySet(direction_domain)
correct_direction.set_value_at(0, 0)
correct_direction.set_value_at(1, 1)

dangerously_close = CalculatedFuzzySet(distance_domain)
dangerously_close.set_calculated_memberships("l", alpha=0.02, beta=0.05)

close = CalculatedFuzzySet(distance_domain)
close.set_calculated_memberships("l", alpha=0.05, beta=0.07)

# not_close = CalculatedFuzzySet(distance_domain)
# not_close.set_calculated_memberships("gamma", alpha=0.5, beta=0.7)

not_close = zadeh_not(close)
not_dangerously_close = zadeh_not(dangerously_close)

small_velocity = CalculatedFuzzySet(velocity_domain)
small_velocity.set_calculated_memberships("l", alpha=0.2, beta=0.84)

large_velocity = CalculatedFuzzySet(velocity_domain)
large_velocity.set_calculated_memberships("gamma", alpha=0.68, beta=0.7)

large_acceleration = CalculatedFuzzySet(acceleration_domain)
large_acceleration.set_calculated_memberships("gamma", alpha=0.68, beta=0.7)

sharp_right = CalculatedFuzzySet(angle_domain)
sharp_right.set_calculated_memberships("l", alpha=0.1, beta=0.2)

sharp_left = CalculatedFuzzySet(angle_domain)
sharp_left.set_calculated_memberships("gamma", alpha=0.8, beta=0.9)

keep_direction = MutableFuzzySet(angle_domain)
for (idx, element) in enumerate(keep_direction.domain.domain_elements):
	if element > -5 and element < 5:
		keep_direction.memberships[idx] = 1
	else:
		keep_direction.memberships[idx] = 0
keep_direction.update_member_dict()


universal_velocity = MutableFuzzySet(velocity_domain)
for (idx, element) in enumerate(universal_velocity.domain.domain_elements):
	universal_velocity.memberships[idx] = 1
universal_velocity.update_member_dict()

universal_distance = MutableFuzzySet(distance_domain)
for (idx, element) in enumerate(universal_distance.domain.domain_elements):
	universal_distance.memberships[idx] = 1
universal_distance.update_member_dict()


universal_distance_with_a_twist = MutableFuzzySet(distance_domain)
for (idx, element) in enumerate(universal_distance_with_a_twist.domain.domain_elements):
	if element == 23:
		universal_distance_with_a_twist.memberships[idx] = 0.5
	else:
		universal_distance_with_a_twist.memberships[idx] = 1
universal_distance_with_a_twist.update_member_dict()


acceleration_rule = MutableFuzzySet(acceleration_domain)
for (idx, element) in enumerate(acceleration_rule.domain.domain_elements):
	if element == 0:
		acceleration_rule.memberships[idx] = 0
	elif element == 8:
		acceleration_rule.memberships[idx] = 0
	else:
		acceleration_rule.memberships[idx] = 0
acceleration_rule.update_member_dict()


my_acc_set = CalculatedFuzzySet(distance_domain)
my_acc_set.set_calculated_memberships("lambda", alpha=0.3, beta=0.5, gamma=0.7)
my_acc_set.update_member_dict()


