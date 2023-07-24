numbers = []

with open('Fakegpsdata.txt', 'r') as file:
    for line in file:
        # Remove any leading/trailing whitespace and split the line into individual numbers
        line = line.strip()
        nums = line.split(',')

        # Convert each number from string to float and add it to the array
        for num in nums:
            numbers.append(float(num))

print(numbers[0], numbers[1], numbers[2])
