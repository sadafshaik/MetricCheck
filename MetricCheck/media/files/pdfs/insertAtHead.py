# class Node:
#     def __init__(self, value):
#         self.value = value
#         self.nextElement = None
    
# class LinkedList:
#     def __init__(self):
#         self.headNode = None
    
#     def getHead(self):
#         return self.headNode

#     def printList(self):
#         if self.isEmpty():
#             print("The list is empty")
#             return False
        
#         temp = self.headNode
#         while temp.nextElement != None:
#             print(temp.value, end="--->")
#             temp = temp.nextElement
#         print(temp.value, end="---> None")

#         return True

#     def isEmpty(self):
#         if self.headNode == None:
#             return True
#         return False

    # def insertAtHead(self, value):
    #     tempNode = Node(value)
    #     tempNode.nextElement = self.headNode
    #     self.headNode = tempNode
    #     return self.headNode
    
#     def insertAtTail(self, value):
#         new = Node(value)
#         if self.headNode == None:
#             self.headNode = new
#             return False
#         tempNode = self.headNode
#         while tempNode.nextElement != None:
#             tempNode = tempNode.nextElement
#         tempNode.nextElement = new
#         return


from LinkedListBase import genList, LinkedListNode, printList, reverseList


def searchList(head, searchElement):
    tempNode = head
    while tempNode != None:
        if tempNode.val == searchElement:
            print("Element is found")
            return True
        else:
            tempNode = tempNode.next
    return False


def insertAtTail(head, value):
    new = LinkedListNode(value)
    if head == None:
        head = new
        return False
    tempNode = head
    while tempNode.next != None:
        tempNode = tempNode.next
    tempNode.next = new

def deleteAtHead(head):
    first = head
    if first is not None:
        head = first.next
        first.next = None
    printList(head)

def reverse(head):
    prev = None
    current = head
    next = None

    while current != None:
        next = current.next
        current.next = prev
        prev = current 
        current = next 

        head = prev

    printList(head)

head = genList()
reverse(head)

# deleteAtHead(head)




# for i in range(1,10):
#     llist.insertAtTail(i)


# print(searchList(head, 8))

# insertAtTail(head, 10)
# printList(reverseList(head))