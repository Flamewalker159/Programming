def reverse_list(nums):
    n = len(nums)
    for i in range(n // 2):
        temp = nums[i]
        nums[i] = nums[n - 1 - i]
        nums[n - 1 - i] = temp
    return nums

arr = [1, 2, 3, 4, 5]
reverse_list(arr)
print(arr)