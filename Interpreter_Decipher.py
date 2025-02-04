#------TreeNode
class TreeNode:
    def __init__(self, srcToken):
        self.value = srcToken[0]
        self.token = srcToken[1]
        self.left = None
        self.right = None

#-----Parsing

#This function might be just me rewriting the previos function
def ParseEX(srcList, p1 = 0): #p1 is really high to ensure that at the start we go in the else statement.
    priority = {"+": 1, "-": 1, "*": 2, "/": 2, "(": 3, ")":0}
    if srcList[0][1] == "NUMB" or srcList[0][1] == "LPRAM" or srcList[0][1] == "SUB": # 3 + 4 is in recursion or (
        leftTree = TreeNode(srcList[0])
        srcList.pop(0)
    if leftTree.token == "SUB":
        #Push to recursion and when "-" is reached.
        rightTree = ParseEX(srcList,4)
        #make the negative in leftTree an operator
        op = leftTree
        op.right = rightTree
        #Make from  - -> 5 to 0 <- - -> 5
        op.left = TreeNode(["0", "NUMB"])
        #Store the new Binary three node in to leftTree
        leftTree = op
        #element added to the rightside of negative is already poped in the recursion
    #If LeftTree is "("
    if leftTree.token == "LPRAM":
        #Push to recursion and when "(" is reached, push out when ")" is reached
        rightTree = ParseEX(srcList,0)
        #set the result to new leftTree
        leftTree = rightTree
        srcList.pop(0) #Remove ")"
    while len(srcList) > 0:
        
        if len(srcList) <= 1:
            #In case srcList is 0 here just return the leftTree
            if len(srcList) == 0:
                return leftTree
            value =  TreeNode(srcList[0])
            if value.token == "RPRAM":
                #Return the complete node made in the parenthesis
                return leftTree
            srcList.pop(0)
            
            return value
        else:  
            p2 = priority.get(TreeNode(srcList[0]).value, 0)  # Get priority of the current token
            if p1 >= p2:
                #node = TreeNode(srcList[0])
                #return node
                return leftTree
            else:
                op = TreeNode(srcList[0])
                srcList.pop(0)
                op.left = leftTree  # Assign leftTree as left child of the operator node
                op.right = ParseEX(srcList, priority.get(op.value, 0))  # Parse right subtree recursively
                leftTree = op  # Update leftTree to be the operator node   
    return leftTree
  
    
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
        
def decipher(babyExp):
    dictionary = {"pee": "+", "gah": "-", "milk":"*", "heh":"/", "mama":"(", "dada": ")", 
                  "b": "0",
                  "ba": "1",
                  "baa": "2",
                  "baaa": "3",
                  "baaaa": "4",
                  "baaaaa": "5",
                  "baaaaaa": "6",
                  "baaaaaaa": "7",
                  "baaaaaaaa": "8",
                  "baaaaaaaaa": "9"
                  }
    srcCode = ""
    i =0
    #Loop through the entire string
    while i < len(babyExp):
        #initiate "word" to empty at start
        word = ""
        #loop through array to find first expression
        while i < len(babyExp):
            if babyExp[i] == " ":
                i += 1
            #add to word a letter from index 0 of expression string
            word += babyExp[i]
            #if the given word is in dictionary key then convert it to operations
            if word in dictionary.keys():
                if word == "b":
                    #If word is just b then get all if any "a"'s that go with it and add them to the word
                    word += getAllAs(babyExp[i+1:])
                    #After all the "a"'s are set, increament i to the last "a"
                    i += len(word)-1
                #set srcCode with operator from dictonary at given word
                srcCode += dictionary[word]
                #increament "i" to next letter
                i += 1
                break
            #increament "i" to next letter
            i += 1
    return srcCode  
def getAllAs(inputString):
    aString = ""
    for v in inputString:
        if v == "a":
            aString = aString + v
        else:
            return aString
    return aString
    
    

def main():
    print("\nHello baby language.\nEnter baby exp and see what you get.")
    while True:
        babyExp = input(">>> ")
        if babyExp.strip() == "poopoo":
            break
        srcCode = decipher(babyExp)
        print("Interpreted as: ", srcCode)
        srcList = tokeniz(srcCode)
        rootNode = ParseEX(srcList)
        result = evaluateTree(rootNode)
        print("The result is: ", result)
    print("Now it is time to go poo poo.")
main()
