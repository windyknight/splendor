from enum import Enum

class InstrumentType(Enum):
    '''
    Defines three types for musical instruments.
    '''
    PERCUSSION = 'p'
    STRINGS = 's'
    WIND = 'w'    

class Instrument:
    '''
    This defines a musical instrument with the name of
    the instrument and its classification.
    '''
    def __init__(self, name, classification):
        '''
        Creates a new instrument. The name and
        classification of the instrument are required
        parameters.
        '''
        self.name = name
        if isinstance(classification, InstrumentType):
            self.classification = classification
        else:
            raise ValueError("Invalid value for instrument type: {}".format(classification))

    def getClassification(self):
        '''
        Returns the classification of the musical instrument.
        '''
        return self.classification

    def getName(self):
        '''
        Returns the name of the musical instrument.
        '''
        return self.name

    def setClassification(self, classification):
        '''
        Sets the classification of the musical instrument.
        '''
        if isinstance(classification, InstrumentType):
            self.classification = classification
        else:
            raise ValueError("Invalid value for instrument type: {}".format(classification))

    def setName(self, name):
        '''
        Sets the name of the musical instrument.
        '''
        self.name = name

    def __gt__(self, other):
        '''
        Convenience function for comparison between
        instruments.
        '''
        return self.name > other.getName()

    def __lt__(self, other):
        '''
        Convenience function for comparison between
        instruments.
        '''
        return self.name < other.getName()

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
    INSTRUCTIONS: As a class, write the methods and the
    documentation for these for a fully-working
    singly-linked list.
    
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
            # insert more code here
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
        # insert more code here
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
        current = head
        size = 0
        while current is not None:
            size += 1
            current = current.getNext()
        return size
##        return self.size
    def getSize(self):
        return self.size

    def countInstances(self, data):
        # Count the number of times
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
        curr = self.head
        while curr is not None:
            yield curr.getData()
            curr = curr.getNext()

    def emptyOut(self):
        while self.head is not None:
            self.delete(self.head.getData())
        self.size = 0

    def head(self):
        return self.head

    def insert(self):
        pass

class Stack(SLList):
    def __init__(self):
        super().__init__()

    def push(self, data):
        super().insertAtHead(Node(data))

    def pop(self):
        data = super().head()
        if data is not None:
            data = data.getData()
            super().delete(data)
        return data

    def top(self):
        if super().head() is not None:
            return super().head().getData()
        else:
            return None

    def getSize(self):
        return super().getSize()

    def empty(self):
        return self.getSize() == 0

    def read(self):
        tmp = [i for i in super().read()]
        return tmp

    def emptyOut(self):
        super().emptyOut()

    def search(self, data):
        try:
            super.search(data)
            return True
        except ValueError:
            return False










