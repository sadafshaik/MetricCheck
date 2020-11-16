from LinkedListBase import genList, LinkedListNode


def cycleCheck(node):
    slow = fast = node

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
             return True
    return False


head = genList()

node = head
node.next.next.next.next = head

print(cycleCheck(head))






