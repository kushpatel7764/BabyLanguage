Author: Kush Patel 

Overview: The project implements a basic programing language calculator that parses mathematical expressions, builds a binary tree from the expression, and evaluates it.

  TreeNode Class: Represents nodes in a binary tree, with a value (operator or number), token, and pointers to left and right children.
  Parsing: The ParseEX function recursively parses a tokenized expression to build a binary tree, handling operators and parentheses based on precedence.
  Evaluation: The evaluateTree function recursively evaluates the expression by performing the necessary arithmetic operations on the tree.
  Tokenization: The tokeniz function breaks a string into tokens (numbers, operators) and assigns them appropriate labels like NUMB, PLUS, SUB.
  Baby Language Translation: The decipher function converts baby language-like expressions into mathematical expressions using a dictionary of mappings.
  Main Function: Handles user input, converts it using decipher, tokenizes it, parses it into a tree, evaluates the expression, and outputs the result.
Overall, this is a calculator program with support for baby language-like expressions that are translated into mathematical operations.

Guide:
