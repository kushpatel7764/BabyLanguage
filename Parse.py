#------TreeNode
class TreeNode:
    def __init__(self, srcToken):
        self.value = srcToken[0]
        self.token = srcToken[1]
        self.left = None
        self.right = None



#-----Parsing
""" 
Plan: Make smaller nodes with first. Then add them to a bigger node. 
"""

#Set smaller tree nodes.
def setLowerNodes(From, OgFOR = None, For = None):
    #from = srcList
    #for = priority
    priority = {"+": 3, "-": 3, "*": 2, "/": 2, "(": 1}
    #Base Case
    amountOfListLeft = 0
    for item in From:
        if isinstance(item, list):
            amountOfListLeft += 1
    if (amountOfListLeft <= 2):
        return From
    

    #Check to make nodes from given priority.
    if (For == None):
        if (From.__contains__(["(", "LPRAM"])):
            start = From.index(["(", "LPRAM"])
            end = From.index([")","RPRAM"])
            arrayInPRAM = From[start+1:end] #get array from start until end but not end.
            rootOfPRAM = ParseEX(arrayInPRAM)
            #Connect root node, anywhere from start and end of from. 
            From[start] = rootOfPRAM
            #Remove all of Parenthesis. 
            del From[start+1:end+1] #start + 1 makes sure that newly added node is not removed. end + 1 because end is excluded. 
            return setLowerNodes(From,OgFOR = None, For = None)
        elif (From.__contains__(["/", "DIV"])):
            For = From.index(["/", "DIV"])
            OgFOR = For
        elif (From.__contains__(["*", "MULTI"])):
            For = From.index(["*", "MULTI"])
            OgFOR = For
        elif (From.__contains__(["+", "PLUS"])):
            For = From.index(["+", "PLUS"])
            OgFOR = For
        elif (From.__contains__(["-", "SUB"])):
            For = From.index(["-", "SUB"])
            OgFOR = For
        else:
            return None

    
    if (For == 0):
        #TODO: Check for invalid input here 
        if (isinstance(From[OgFOR-1], list)): #If is here incase a TreeNode is already present from previous calculation
            leftTree = TreeNode(From[OgFOR - 1])
        else:
            leftTree = From[OgFOR - 1]
        Operator = TreeNode(From[OgFOR])
        if (isinstance(From[OgFOR+1], list)):
            rightTree = TreeNode(From[OgFOR + 1])
        else:
            rightTree = From[OgFOR+1]
        Operator.left = leftTree
        Operator.right = rightTree 
        #Remove the old lists from list.
        From.pop(OgFOR + 1)
        From.pop(OgFOR - 1)
        #Put root node in srcList at the previous index
        From[OgFOR - 1] = Operator
        return setLowerNodes(From,OgFOR = None, For = None)

    if (For != None and OgFOR != None):
        For = For -  1
        return setLowerNodes(From,OgFOR, For)
    

#This function might be just me rewriting the previos function
def ParseEX(srcList):
     #Base Case: No need to do set tree stuff if only one thing in list. 
    if (len(srcList) == 1):
        return TreeNode(srcList[0])
    
    setLowerNodes(srcList)

    #If setLowerNodes only returns a srcList with only 1 node then return that three node
    if (len(srcList) == 1):
        return srcList[0]
   
    #Set Left node depending on its instance
    if (isinstance(srcList[0], list)):
        LeftTree = TreeNode(srcList[0])
    else:
        LeftTree = srcList[0]
    #Set Operator node
    Operator = TreeNode(srcList[1])
    #Set Right node
    if (isinstance(srcList[2], list)):
        RightTree = TreeNode(srcList[2])
    else:
        RightTree = srcList[2]
    #Once set, remove the two nodes from the list 
    srcList.pop(1); 
    srcList.pop(0); 
    #Connect the left and right nodes to the operator
    Operator.left = LeftTree
    Operator.right = RightTree
    #Return the root node
    return Operator


#-----Tokeniz
def tokeniz(src):
    to_return_list = []
    for(i,v) in enumerate(src):
        to_seek_list=[]
        to_seek_list.append(v)
        if v == " ":
            continue
        to_seek_list.append(find_token(v))

        if len(to_return_list) != 0 and (to_seek_list[1] == "NUMB" or to_seek_list[1] == "PERD"):
            if check_prev(to_return_list):
                to_return_list[-1][0]= to_return_list[-1][0]+v
                continue

        to_return_list.append(to_seek_list)
    return to_return_list

def find_token(token):
    match token:
        case "(": return "LPRAM"
        case "+": return "PLUS"
        case "-": return "SUB"
        case ")": return "RPRAM"
        case "*": return "MULTI"
        case "/": return "DIV"
        case ".": return "PERD"
        case _: 
            if token.isdigit():
                return "NUMB"
            else:
                return "UNKNOWN"

def check_prev(list):
    if (list[-1][1] == "NUMB" or list[-1][1] == "PERD"):
        return True
    else:
        return False
        

#Email: pRathaur@student.bridgew.edu
#Email: jdompreh@student.bridgew.edu    
    
#-----Evaluate tree
def evaluateTree(rootNode):
    #rootNode is there and is not none.
    if rootNode == None:
        return 0
    
    #return rootNode value if it is a digit 
    noPeriodrootNode = rootNode.value.replace(".", "")
    if noPeriodrootNode.isdigit(): #Root node is always a operator, if not then just return that number 
        return float(rootNode.value) 
    
    #If rootNode.value is not an digit then it must be a operator 
    left_value = evaluateTree(rootNode.left) #go in rootNode left and do all the calculations in it for left side
    right_value = evaluateTree(rootNode.right) #go in rootNode right and do all the calculations in it for the right side

    #Find which Operator and do the operation
    if rootNode.value == '+':
        return left_value + right_value
    elif rootNode.value == '-':
        return left_value - right_value
    elif rootNode.value == '*':
        return left_value * right_value
    elif rootNode.value == '/':
        if right_value == 0:
            return "Error: Division by zero"
        return left_value / right_value
    

    

def main():
    #Decimal not work.
    while 1:
        src = input(">> ")
        if src == "/quit":
            return
        srcList = tokeniz(src)
        rootNode = ParseEX(srcList)
        result = evaluateTree(rootNode)
        print(result)


main()
