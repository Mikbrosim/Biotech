class Node:
    def __init__(self, name = None, parent = None, parentLength = 0):
        self.name = name
        self.child = []
        self.contains = []
        self.parent = parent
        self.parentLength = parentLength

    @property
    def distToTop(self):
        if self.parent == None:
            return 0
        return self.parentLength + self.parent.distToTop

    @property
    def tree(self):
        if self.child == []:
            return self.name
        return "  >"+"\n  >".join(child.tree + " " + str(child.parent.distToTop-child.distToTop) for child in self.child)

class Phylogenetic:
    def dnaDif(self, name, secondName):
        # Return the difference in two sequences, by name
        return sum([self.sequence[name][i]!=self.sequence[secondName][i] for i in range(len(self.sequence[name]))])

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

    def __init__(self, sequence):
        self.sequence = sequence
        self.newNames = self.sequence.keys()
        self.table = {}

        # Make sure the sequences are the same lengths, to ensure not errors in dnaDif
        if len(set(map(len,self.sequence.values())))!=1:
            return False

        self.makeTable()
        name, secondName, forskel = self.minInTable()
        root1 = Node()
        root1.child = [Node(name, root1, root1.distToTop-forskel/2), Node(secondName, root1, root1.distToTop-forskel/2)]
        root1.contains.append(name)
        root1.contains.append(secondName)
        #print("\n"*3+str(self.table))
        print("\n"+root1.tree)

        self.makeTable()
        name, secondName, forskel = self.minInTable()
        root2 = Node()
        root2.child = [Node(name, root2, root2.distToTop-forskel/2), Node(secondName, root2, root2.distToTop-forskel/2)]
        root2.contains.append(name)
        root2.contains.append(secondName)
        #print("\n"*3+str(self.table))
        print("\n"+root2.tree)

        self.makeTable()
        name, secondName, forskel = self.minInTable()
        root3 = Node()
        root3.child = [Node(name, root3, root3.distToTop-forskel/2), Node(secondName, root3, root3.distToTop-forskel/2)]
        root3.contains.append(name)
        root3.contains.append(secondName)
        #print("\n"*3+str(self.table))
        print("\n"+root3.tree)

        self.makeTable()
        name, secondName, forskel = self.minInTable()
        root4 = Node()
        root4.child = [Node(name, root4, root4.distToTop-forskel/2), Node(secondName, root4, root4.distToTop-forskel/2)]
        root4.contains.append(name)
        root4.contains.append(secondName)
        #print("\n"*3+str(self.table))
        print("\n"+root4.tree)

        self.makeTable()
        name, secondName, forskel = self.minInTable()
        root5 = Node()
        root5.child = [Node(name, root5, root5.distToTop-forskel/2), Node(secondName, root5, root5.distToTop-forskel/2)]
        root5.contains.append(name)
        root5.contains.append(secondName)
        #print("\n"*3+str(self.table))
        print("\n"+root5.tree)

sequence = {
"Sibirisk tiger":"GCACCGTACCCCCCTCACTTTGTGGCACCTCTATATAATGCTACTAGGCTGCCG",
"Sydkinesisk tiger":"ACGCCGCACTCCCTCCGCTTTGTGGCATCTCTACATGATGCCATCAAGCCACTG",
"Indokinesisk tiger I":"GTACCGCACCCCCCTCGCTTTATAGCACTTCTATATAATGCTACTAGGCTGCTG",
"Indokinesisk tiger II":"GCGCCGCACCCCCCTCGCTTTGTGATATCTTTACGTAATGCTACTAGGCTGCCG",
"Sumatra tiger":"ACGCCGCACCCCCTTCGCTTTGCGGCGTCTCTACATAACGCCATTAGGTTGCTG",
"Bengalsk tiger":"GCGCCGGACCCCCCTTGCTCTGTGGCATCTCTACATAACGTCATTAGACTGCTG"
}

Phylogenetic(sequence)
