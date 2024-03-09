import random

def generate_random_number(low, high):
    return random.uniform(low, high)

# Example usage:
low_value = 90
high_value = 130
low_value1 = 70
high_value1 = 90
random_number = generate_random_number(low_value, high_value)

for i in range(1,8):
    print("2024/02/"+str(i)+":" + str(int(generate_random_number(low_value, high_value)))+"//"+str(int(generate_random_number(low_value1, high_value1)))+" mmHg")
low_value = 110
high_value = 130
low_value1 = 70
high_value1 = 90
for i in range(8,15):
    print("2024/02/"+str(i)+":" + str(int(generate_random_number(low_value, high_value)))+"//"+str(int(generate_random_number(low_value1, high_value1)))+" mmHg")
low_value = 130
high_value = 150
low_value1 = 90
high_value1 = 100
for i in range(15,23):
    print("2024/02/"+str(i)+":" + str(int(generate_random_number(low_value, high_value)))+"//"+str(int(generate_random_number(low_value1, high_value1)))+" mmHg")
low_value = 130
high_value = 160
low_value1 = 90
high_value1 = 110
for i in range(23,32):
    print("2024/02/"+str(i)+":" + str(int(generate_random_number(low_value, high_value)))+"//"+str(int(generate_random_number(low_value1, high_value1)))+" mmHg")