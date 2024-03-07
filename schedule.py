class Schedule(dict):
    def __init__(self, sched=None):
        if sched is not None: super().__init__(sched)

    @classmethod
    def GenerateRandom(cls, BR_matches, SR_matches, random):
        rtn = cls()
        ## Generates a schedule randomly, given a number of matches to be allocated
        rtn.random = random
        rtn.BR_matches = BR_matches
        rtn.SR_matches = SR_matches
        # First 7 rounds: 2 BR courts, 1 SR court
        for i in range(7):
            m1, m2, m3 = rtn.PopUniqueMatches( (2,1) )
            rtn[f'Round {i+1}'] = {
                'Court 1 (BR)': m1,
                'Court 2 (BR)': m2,
                'Court 3 (SR)': m3
            }
        # Last 7 rounds: 2 SR courts, 1 BR court
        for i in range(7):
            m1, m2, m3 = rtn.PopUniqueMatches( (1,2) )
            rtn[f'Round {i+8}'] = {
                'Court 1 (BR)': m1,
                'Court 2 (SR)': m2,
                'Court 3 (SR)': m3
            }
        if len(BR_matches) + len(SR_matches) > 0:
            # clashes have meant the schedule hasn't been filled, raise an error
            raise RuntimeError("Random allocation has left unallocated matches due to clashes. Run again.")
        return rtn

    def PopUniqueMatches( self, n_matches ):
        # n_matches tuple specifying how many BR matches and how many SR matches to pop
        matches = []
        veto = []
        # function to return the list to be popped from at any point:
        def MatchList():
            if len(matches) >= n_matches[0]:
                return self.SR_matches
            return self.BR_matches        
        # Loop through the number of required matches and use the pop functions to pull from the
        # relevant list
        for i in range(sum(n_matches)):
            # pop match
            match_ = self.PopRandomListElem( MatchList(), veto )
            # update veto
            if match_ is not None:
                for team in match_: veto.append(team)
            # save the popped match
            matches.append(match_)
        return matches

    def PopRandomListElem( self, elems, veto=[] ):
        pop_index = self.PickPopIndex(elems, veto)
        if pop_index is None: return None
        return elems.pop(pop_index)

    def PickPopIndex( self, elems, veto=[], indices=None ):
        # Manipulate a list of indices rather than the full list to preserve
        # index of 'elems' list after popping from list copies
        if indices is None: indices = [i for i,_ in enumerate(elems)]
        # base case
        if len(indices) < 1: return None 
        # pick a random index
        rand_index = self.random.randint(0, len(indices)-1)
        # check if a team in the veto list is in the selected match
        selected_match = elems[indices[rand_index]]
        overlap = set(veto) & set(selected_match)
        if len(overlap) > 0:
            # we have a clash: recurse to try again
            reduced_indices = indices.copy()
            reduced_indices.pop(rand_index)
            return self.PickPopIndex( elems, veto, reduced_indices )
        # else: no clash, use this index
        return indices[rand_index]

    def GetTeamSchedule(self, team):
        rtn = [[] for i in range(len(self))]
        for round_i, round_matches in enumerate(self.values()):
            for court, match_ in round_matches.items():
                if match_ is not None and team in match_:
                    rtn[round_i].append((court, match_))
        return rtn

    def GetTeamSchedules(self, teams):
        return { team : self.GetTeamSchedule(team) for team in teams }

    def __str__(self):
        rtn = ""
        for round_no, round_matches in self.items():
            rtn += f"{' '+round_no+' ':=^20s}\n"
            for court_no, court_match in round_matches.items():
                rtn += f"{court_no}: " + (
                    f"{court_match[0]} v  {court_match[1]}\n" if court_match is not None else "no match\n"
                )
        return rtn
