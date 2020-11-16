from heapq import heappush as push, heappop as pop
# def minWindow(s, t):
#     def checkIfTargetPresent(i, j, t):
#         targetDic = {}
#         for char in t:
#             targetDic[char] = 1
#         substr = s[i: j]
#         for char in substr:
#             if char in targetDic:
#                 del targetDic[char]
#         return len(targetDic) == 0
        
#     # two pointers at 0
#     i = j = 0
#     flag = True
#     minHeap = []
#     # iterate using while
#     while(i < len(s) or j < len(s)):
#         if flag:
#             # incr j if current window doesn't have target chars
#             if j < len(s):
#                 j += 1
#             else:
#                 break
#         else:                
#             # if current window has target, incr i to drecrese window
#             i += 1
#         if checkIfTargetPresent(i, j, t):
#             # push into heap
#             push(minHeap, (len(s[i:j]), s[i:j]))
#             flag = False # decrement the window to get min suybstr
#         else:
#             flag = True # increment the window
            
#     # return minlen

#     return pop(minHeap)[1] if len(minHeap) else ""


# print(minWindow("a", "b"))

from heapq import heappush as push, heappop as pop
def kthLargest(nums, k):
    maxHeap= []
    for num in nums:
        push(maxHeap, -num)
    temp = float("-inf")
    for i in range(k):
        temp = pop(maxHeap)
    return -temp   


print(kthLargest([1,2,3,4,5,6,7], 2))



