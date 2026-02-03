def avg(nums):
    total = 0
    for n in nums:
        total += n
    return total / len(nums)

def read_file(path):
    f = open(path, "r")
    data = f.read()
    return data

print("Average is " + avg([10, 20, 30]))
