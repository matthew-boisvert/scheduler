
class TimeBlock:
    ''' Time Block: Represents a scheduled event based on its start and end times '''
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __repr__(self):
        return "({0}, {1})".format(self.start, self.end)


class Node:
    ''' Node: Used to represent node in BST '''
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insertIntoBST(bst, timeSlot):
    ''' 
    Insert timeSlot into BST by either merging the timeSlot into an existing
    node or creating a new node
    '''
    # If the time slot intersects with the root node's interval, merge the intervals
    if timeSlot.start <= bst.value.end and bst.value.start <= timeSlot.end:
        bst.value.start = min(timeSlot.start, bst.value.start)
        bst.value.end = max(timeSlot.end, bst.value.end)
    # If the time slot occurs entirely before the root's interval, insert to the left
    elif timeSlot.start <= bst.value.start:
        if bst.left is None:
            bst.left = Node(timeSlot)
        else:
            insertIntoBST(bst.left, timeSlot)
    # If the time slot occurs entirely after the root's interval, insert to the right
    else:
        if bst.right is None:
            bst.right = Node(timeSlot)
        else:
            insertIntoBST(bst.right, timeSlot)


def createBST(busyBlocks, start, end):
    '''
    Merges the TimeBlock lists of multiple entities into a single BST of TimeBlock intervals    

    Preconditions:
        For each TimeBlock in busyBlocks, the end time > the start time
        Each TimeBlock in busyBlocks has a start time that is >= start
        Each TimeBlock in busyBlocks has an end time that is <= end
    '''
    bst = None
    for entityTimes in busyBlocks:
        for timeSlot in entityTimes:
            if bst is None:
                bst = Node(timeSlot)
            else:
                insertIntoBST(bst, timeSlot)
    # Insert sentinel nodes for the start and end times (to make algo easier)
    insertIntoBST(bst, TimeBlock(start - 1, start))
    insertIntoBST(bst, TimeBlock(end, end + 1))
    return bst

def getLatestEnd(bst):
    ''' Returns the most recent end of a TimeBlock in the BST '''
    if bst is None:
        return None
    rightTime = getLatestEnd(bst.right)
    if rightTime is None:
        return bst.value.end
    else:
        return rightTime

def getEarliestStart(bst):
    ''' Returns the earliest start time of a TimeBlock in the BST '''
    if bst is None:
        return None
    leftTime = getEarliestStart(bst.left)
    if leftTime is None:
        return bst.value.start
    else:
        return leftTime

def findEarliestSlot(bst, minDuration):
    '''
    Performs in-order traversal to determine the earliest time slot during which
    all of the entities are free (i.e. this time doesn't intersect with any of the
    timeslots in the BST) for at least minDuration.
    '''
    # Base case: Return None when there are no times that work
    if bst is None:
        return None
    # Attempt to find the earliest slot in the left subtree
    leftOutcome = findEarliestSlot(bst.left, minDuration)
    if leftOutcome is not None:
        return leftOutcome
    # If the left subtree fails, try the current node
    if bst.left is not None:
        # Find the gap between the end of the most recent TimeBlock in the left subtree
        # and the start of the current node
        slotStart = getLatestEnd(bst.left)
        slotLength = bst.value.start - slotStart
        if slotLength >= minDuration:
            return slotStart
    if bst.right is not None:
        # Find the gap between the end of the current node and the earliest TimeBlock in the
        # right subtree
        slotEnd = getEarliestStart(bst.right)
        slotLength = slotEnd - bst.value.end
        if slotLength >= minDuration:
            return bst.value.end
    # If we weren't able to find a slot in the left subtree or the current node, try the right subtree
    return findEarliestSlot(bst.right, minDuration)
             
    
def scheduleEvent(busyBlocks, start, end, minDuration):
     ''' 
     Wrapper function which attempts to schedule an event by merging together all of the busyBlocks
     into a BST and then perform an in-order traversal of the BST to search for the earliest timeslot
     where an event can be scheduled. Returns None if the event cannot be scheduled or an Int representing
     the earliest possible timeslot if it is possible.
     '''
     busyBlockBST = createBST(busyBlocks, start, end)
     return findEarliestSlot(busyBlockBST, minDuration)
