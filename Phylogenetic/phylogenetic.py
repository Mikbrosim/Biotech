class Node:
    upDownSymbols = ["└","┌"]

    def __init__(self, name = None, thisLength = 0, size = 0):
        self.name = name
        self.children = []
        self.thisLength = thisLength
        self.adjustedLength = thisLength
        self.size = size

    def tree(self, i=0, size = None, reversed = False):
        # When the size is None, make sure to get it
        if size == None:
            size = self.size

        # Make sure the number is restrained to 5 characters
        adjustedLengthString = str(self.adjustedLength).ljust(5)[:5]

        # If no children return the minimal branch
        if self.children == []:
            return "  │─" + "─"*8*(size-i+1) + self.name + "\n    " + adjustedLengthString

        # Get the branches of tree
        firstChild = self.children[0].tree(i+1, size, reversed).replace("│─",self.upDownSymbols[    reversed]+"─")
        secondChild= self.children[1].tree(i+1, size, reversed).replace("│─",self.upDownSymbols[not reversed]+"─")

        # Combine branches, and make room for number beneath
        tree = firstChild + "\n│───────┤\n|" + secondChild

        # Make surethe offset is correct
        tree = "\n".join(("  " + line if "│───────┤" == line else "      * " + line) for line in tree.split("\n"))

        # Add the dna difference number to the tree
        tree = "\n".join(line.replace("  * | ", adjustedLengthString) for line in tree.split("\n"))
        return tree

    def prettyTree(self, reversed = False, cut = 3):
        # Remove the stars and shorten the root
        tree = "\n".join(line.replace("*"," ")[cut:] for line in self.tree(reversed = reversed).split("\n"))

        # Split the tree into lines and reverse them if requried
        treeList = tree.split("\n")[::reversed*2-1]

        # Split the lines into individualt characters
        treeList = list(map(list,treeList))

        # Check ever blank space to see whether or not they should have a │
        for i in range(1,len(treeList)):
            for j in range(len(treeList[i])):
                if treeList[i][j] == " ":
                    if len(treeList[i-1])>j and treeList[i-1][j] in ("┌","│","┤"):
                        treeList[i][j] = "│"

        # Assemble the treeList back together
        tree = "\n".join("".join(line) for line in treeList)

        return tree

class UPGMA:
    def dnaDif(self, name, secondName):
        # Return the difference in two sequences, by name
        return sum([self.sequences[name][i]!=self.sequences[secondName][i] for i in range(len(self.sequences[name]))])

    def minInTable(self):
        # Gets the lowest sequence pair for every sequence, and then find the lowest of sequence pair.
        a,(b,c) = min({name:min(self.table[name].items(), key=lambda x: x[1]) for name in self.table}.items(), key=lambda x: x[1][1])
        return a,b,c

    def makeTable(self):
        # If this is the first table, ignore the first part
        if self.table != {}:
            # Get the two sequences with the lowest difference
            name, secondName, difference = self.minInTable()

            # Combine those two names in the list of sequence names
            self.newNames = [name+"|"+secondName] + [_ for _ in self.newNames if _ != name and _ != secondName]

        # Clean the table
        self.table = {}

        # Loop through the sequence names, and create a new table, by getting the genetic differences between the two sequences
        for name in self.newNames:
            # Splitting is needed to take care of averaging of the differences
            _names = name.split("|")
            _tempDict = {}
            for secondName in self.newNames:
                _secondNames = secondName.split("|")

                # Make sure not to check difference between itself, as it would give 0
                if name!=secondName:
                    _tempDict[secondName] = sum(sum(self.dnaDif(_name,_secondName) for _name in _names) for _secondName in _secondNames)/(len(_names)*len(_secondNames))

            # Add the tested sequence into the table
            self.table[name] = _tempDict

    def makeBranch(self, name, difference):
        # Check if leaf is actually a loose branch
        if name in self.looseBranches:
            # Remove the branch from the looseBranches
            newBranch = self.looseBranches.pop(name)

            # Set the branch length
            newBranch.thisLength = difference/2
            newBranch.adjustedLength = newBranch.thisLength - newBranch.children[0].thisLength

            # Set the size of the tree
            newBranch.size = max(newBranch.children, key=lambda x: x.size).size + 1
        else:
            # Create a new leaf
            newBranch = Node(name, difference/2)
        return newBranch

    def __init__(self, sequences):
        self.sequences = sequences
        self.newNames = self.sequences.keys()
        self.table = {}
        self.looseBranches = {}

        # Make sure the sequences are the same lengths, to ensure not errors in dnaDif
        if len(set(map(len,self.sequences.values())))!=1:
            return False

        # Loop throug the sequences to construct a tree
        for i in range(len(self.sequences)-1):
            # Make a comparison table
            self.makeTable()

            # Get the most alike sequences
            name, secondName, difference = self.minInTable()

            # Create a new loose branch
            self.looseBranches[name+"|"+secondName] = Node()
            branch = self.looseBranches[name+"|"+secondName]

            # Add leaves to the branch
            branch.children = [self.makeBranch(name, difference), self.makeBranch(secondName, difference)]

        # The last remaining looseBranch is the root of the tree, and as such the tree is constructed
        self.root = list(self.looseBranches.values())[0]

        # Get the size of the tree
        self.root.size = max(self.root.children, key=lambda x: x.size).size + 1

fromFile = False
if fromFile:
    # Create dict of sequences from 'fas' file
    f = open("seq.fas","r")
    _ = f.read().split("\n")
    sequences = {_[i][1:]:_[i+1] for i in range(0,len(_)-1,2)}
    f.close()
else:
    # Create a manual dict
    sequences = {
    "Sibirisk tiger":"GCACCGTACCCCCCTCACTTTGTGGCACCTCTATATAATGCTACTAGGCTGCCG",
    "Sydkinesisk tiger":"ACGCCGCACTCCCTCCGCTTTGTGGCATCTCTACATGATGCCATCAAGCCACTG",
    "Indokinesisk tiger I":"GTACCGCACCCCCCTCGCTTTATAGCACTTCTATATAATGCTACTAGGCTGCTG",
    "Indokinesisk tiger II":"GCGCCGCACCCCCCTCGCTTTGTGATATCTTTACGTAATGCTACTAGGCTGCCG",
    "Sumatra tiger":"ACGCCGCACCCCCTTCGCTTTGCGGCGTCTCTACATAACGCCATTAGGTTGCTG",
    "Bengalsk tiger":"GCGCCGGACCCCCCTTGCTCTGTGGCATCTCTACATAACGTCATTAGACTGCTG"
    }

# Create the tree
root = UPGMA(sequences).root

# Print the tree
print(root.prettyTree(reversed = False, cut = 6))
