from enum import Enum

class SLLNode:
    '''
    This defines a node in a singly-linked list. The node
    contains a data component and a nextnode reference. By
    default, data and nextnode are None.
    '''
    def __init__(self, data=None, nextnode=None):
        '''
        Creates a new node in the singly-linked list. If
        there is no data or nextnode passed, the values
        default to None.
        '''
        self.data = data
        self.nextnode = nextnode

    def getData(self):
        '''
        Returns the object the node contains.
        '''
        return self.data

    def getNext(self):
        '''
        Returns the reference to the next node.
        '''
        return self.nextnode

    def setData(self, data):
        '''
        Sets the object the node contains.
        '''
        self.data = data

    def setNext(self, nextnode):
        '''
        Sets the reference to the next node.
        '''
        self.nextnode = nextnode

class SLList:
    '''
    Properties of the singly-linked list.
    head: reference to the first node
    '''
    def __init__(self, head = None):
        '''
        Create an empty list if there is no node passed to
        the constructor. Otherwise, create a list with the
        node passed.
        '''
        self.head = head
        if self.head is None:
            self.size = 0
        else:
            self.size = 1

    def insert(self, data):
        '''
        Inserts a node at the end of the list.
        '''
        if isinstance(data, SLLNode):
            if self.head is None:
                self.head = data
            else:
                current = self.head
                while current.getNext() is not None:
                    current = current.getNext()
                current.setNext(data)
            pass
        else:
            newNode = SLLNode(data)
            if self.head is None:
                self.head = newNode
            else:
                current = self.head
                while current.getNext() is not None:
                    current = current.getNext()
                current.setNext(newNode)
        self.size += 1

    def insertAtHead(self, data):
        '''
        Inserts a node at the start of the list.
        '''
        # insert more code here
        if isinstance(data, SLLNode):
            data.setNext(self.head)
            self.head = data
        else:
            newNode = SLLNode(data)
            newNode.setNext(self.head)
            self.head = newNode
        self.size += 1
        pass

    def getSizealt(self):
        '''
        Alternate function for returning the size of the list.
        '''
        current = head
        size = 0
        while current is not None:
            size += 1
            current = current.getNext()
        return size
    def getSize(self):
        '''
        Returns the size of the list.
        '''
        return self.size

    def countInstances(self, data):
        '''
        Returns the number of instances of the data from the list.
        '''
        num = 0
        current = self.head
        if isinstance(data, SLLNode):
            data = self.getData()
        if current.getData() == data:
            num += 1
        while current.getNext() is not None:
            current = current.getNext()
            if current.getData() == data:
                num += 1
        return num
        pass

    def search(self, data):
        '''
        Returns the reference to the node of the given data, otherwise returns a value error.
        '''
        # ValueError("Item {} not found".format(str(data)))
        # should be raised if the data is not found. If it
        # is found, the reference to the node is returned.
        current = self.head
        if isinstance(data, SLLNode):
            data = self.getData()
        if current.getData() == data:
            return current
        while current.getNext() is not None:
            current = current.getNext()
            if current.getData() == data:
                return current
        raise ValueError("Item {} not found".format(str(data)))
        pass

    def insertAfter(self, data, newdata):
        '''
        Inserts the newdata value after the data reference node.
        '''
        # Look for the instance of data and add a new node
        # after it with newdata.
        if not isinstance(newdata, SLLNode):
            newdata = SLLNode(newdata)
        try:
            after = self.search(data)
            if after.getNext() is None:
                after.next(newdata)
            else:
                newdata.setNext(after.getNext())
                after.setNext(newdata)
            self.size += 1
        except ValueError:
            raise ValueError("Item {} not found".format(str(data)))
        pass

    def delete(self, data):
        '''
        Deletes the data from the list.
        '''
        # Hint: you can use search.
        if isinstance(data, SLLNode):
            data = data.getData()
        try:
            current = self.head
            if current.getData() == data:
                self.head = current.getNext()
            else:
                before = current
                current = current.getNext()
                while current is not None:
                    if current.getData() == data:
                        before.setNext(current.getNext())
                    before = before.getNext()
                    current = current.getNext()
            self.size -= 1
        except:
            raise ValueError("Item {} not found".format(str(data)))

    def insertInOrder(self, data):
        '''
        Inserts the data in ascending order.
        '''
        # Insert a new node assuming that the list is in
        # ascending order and the order is preserved.
        current = self.head
        if isinstance(data, SLLNode):
            data = self.getData()
        if current.getData() <= data and current.getNext().getData() >= data:
            self.insertAfter(current, data)
        else:
            while current.getNext() is not None:
                current = current.getNext()
                if current.getData() <= data and current.getNext().getData() >= data:
                    self.insertAfter(current, data)
            self.insert(data)
        pass
        self.size += 1

    def read(self):
        '''
        Returns the values of the list.
        '''
        curr = self.head
        while curr is not None:
            yield curr.getData()
            curr = curr.getNext()

    def emptyOut(self):
        '''
        Deletes the whole list.
        '''
        while self.head is not None:
            self.delete(self.head.getData())
        self.size = 0

    def head(self):
        '''
        Returns the reference to head.
        '''
        return self.head

class Stack(SLList):
    '''
    This class defines the properties of a Stack.
    '''
    def __init__(self):
        '''
        Creates a stack based from the SLList super class.
        '''
        super().__init__()

    def push(self, data):
        '''
        Inserts the data to head, and pushing the list to the right.
        '''
        super().insertAtHead(SLLNode(data))

    def pop(self):
        '''
        Deletes the value at head and returns the reference of head.
        '''
        data = super().head()
        if data is not None:
            data = data.getData()
            super().delete(data)
        return data

    def top(self):
        '''
        Returns the value at head.
        '''
        if super().head() is not None:
            return super().head().getData()
        else:
            return None

    def getSize(self):
        '''
        Returns the size of the stack.
        '''
        return super().getSize()

    def empty(self):
        '''
        Returns the size of stack to zero.
        '''
        return self.getSize() == 0

    def read(self):
        '''
        Returns the data in the stack.
        '''
        tmp = [i for i in super().read()]
        return tmp

    def emptyOut(self):
        '''
        Deletes the data in the stack.
        '''
        super().emptyOut()

    def search(self, data):
        '''
        Returns the reference of the data, otherwise returns false.
        '''
        try:
            super.search(data)
            return True
        except ValueError:
            return False










