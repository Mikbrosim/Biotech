class Node:
    def __init__(self, name = None, thisLength = 0, longestWayToLeaf = 0):
        self.name = name
        self.children = []
        self.thisLength = thisLength
        self.adjustedLength = thisLength
        self.longestWayToLeaf = longestWayToLeaf

    def tree(self, i=0, longestWayToLeaf = None):
        if longestWayToLeaf == None:
            longestWayToLeaf = self.longestWayToLeaf

        adjustedLengthString = str(self.adjustedLength).ljust(5)[:5]

        # If no children return the minimal branch
        if self.children == []:
            return "    " + adjustedLengthString + "\n  │─" + "─"*8*(longestWayToLeaf-i+1) + self.name

        # Get the branches of tree
        firstChild = self.children[0].tree(i+1, longestWayToLeaf).replace("│─","┌─")
        secondChild= self.children[1].tree(i+1, longestWayToLeaf).replace("│─","└─")

        # Combine branches, and make room for number beneath
        tree = firstChild + "\n│───────┤\n|" + secondChild

        # Make surethe offset is correct
        tree = "\n".join(("  " + line if "│───────┤" == line else "      * " + line) for line in tree.split("\n"))

        # Add the dna difference number to the tree
        tree = "\n".join(line.replace("  * | ", adjustedLengthString) for line in tree.split("\n"))
        return tree

    def treePrinter(self):
        tree = "\n".join(line.replace("*"," ")[3:] for line in self.tree().split("\n"))
        treeText = tree.split("\n")
        treeText = list(line.ljust(max(map(len,treeText))) for line in treeText)
        treeText = list(map(list,treeText))

        for i in range(1,len(treeText)):
            for j in range(len(treeText[i])):
                if treeText[i][j] == " ":
                    if treeText[i-1][j] in ("┌","│","┤"):
                        treeText[i][j] = "│"

        tree = "\n".join("".join(line) for line in treeText)

        return tree

class Phylogenetic:
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
            name, secondName, forskel = self.minInTable()

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

    def __init__(self, sequences):
        self.sequences = sequences
        self.newNames = self.sequences.keys()
        self.table = {}
        self.looseBranches = {}

        # Make sure the sequences are the same lengths, to ensure not errors in dnaDif
        if len(set(map(len,self.sequences.values())))!=1:
            return False

        for i in range(len(self.sequences)-1):
            self.makeTable()
            name, secondName, forskel = self.minInTable()

            self.looseBranches[name+"|"+secondName] = Node()
            branch = self.looseBranches[name+"|"+secondName]

            if name in self.looseBranches:
                firstBranch = self.looseBranches.pop(name)
                firstBranch.thisLength = forskel/2
                firstBranch.adjustedLength = firstBranch.thisLength - firstBranch.children[0].thisLength
                firstBranch.longestWayToLeaf = max(firstBranch.children, key=lambda x: x.longestWayToLeaf).longestWayToLeaf + 1
            else:
                firstBranch = Node(name, forskel/2)

            if secondName in self.looseBranches:
                secondBranch = self.looseBranches.pop(secondName)
                secondBranch.thisLength = forskel/2
                secondBranch.adjustedLength = secondBranch.thisLength - secondBranch.children[0].thisLength
                secondBranch.longestWayToLeaf = max(secondBranch.children, key=lambda x: x.longestWayToLeaf).longestWayToLeaf + 1
            else:
                secondBranch = Node(secondName, forskel/2)

            branch.children = [firstBranch, secondBranch]

        root = list(self.looseBranches.values())[0]
        root.longestWayToLeaf = max(root.children, key=lambda x: x.longestWayToLeaf).longestWayToLeaf + 1

        print(root.treePrinter())

sequences = {
"Sibirisk tiger":"GCACCGTACCCCCCTCACTTTGTGGCACCTCTATATAATGCTACTAGGCTGCCG",
"Sydkinesisk tiger":"ACGCCGCACTCCCTCCGCTTTGTGGCATCTCTACATGATGCCATCAAGCCACTG",
"Indokinesisk tiger I":"GTACCGCACCCCCCTCGCTTTATAGCACTTCTATATAATGCTACTAGGCTGCTG",
"Indokinesisk tiger II":"GCGCCGCACCCCCCTCGCTTTGTGATATCTTTACGTAATGCTACTAGGCTGCCG",
"Sumatra tiger":"ACGCCGCACCCCCTTCGCTTTGCGGCGTCTCTACATAACGCCATTAGGTTGCTG",
"Bengalsk tiger":"GCGCCGGACCCCCCTTGCTCTGTGGCATCTCTACATAACGTCATTAGACTGCTG"
}

Phylogenetic(sequences)
