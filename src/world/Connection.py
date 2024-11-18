class Connection:
    def __init__ (self, target, currentInterval:range):
        self.target = target
        self.currentInterval = currentInterval  # Originating Node

    def getIntervalDistance(self, prevInterval) -> int:  # I took this from SO
        # sort the two ranges such that the range with smaller first element
        # is assigned to x and the bigger one is assigned to y
        r1 = [prevInterval[0], prevInterval[-1]]
        r2 = [self.currentInterval[0], self.currentInterval[-1]]
        x, y = sorted((r1, r2))

        #now if x[1] lies between x[0] and y[0](x[1] != y[0] but can be equal to x[0])
        #then the ranges are not overlapping and return the differnce of y[0] and x[1]
        #otherwise return 0 
        if x[0] <= x[1] < y[0] and all( y[0] <= y[1] for y in (r1,r2)):
            return y[0] - x[1]
        return 0