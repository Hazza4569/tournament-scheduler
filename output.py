def PrintSchedule( schedule ):
# Pretty print schedule
    for round_no, round_matches in schedule.items():
        print(f"{' '+round_no+' ':=^20s}")
        for court_no, court_match in round_matches.items():
            if court_match is not None:
                print(f"{court_no}: {court_match[0]} v  {court_match[1]}")
            else: print(f"{court_no}: no match")

def CourtFormat( court_raw ):
    return court_raw.lower().replace('br','Birmingham rules').replace('sr','Sheffield rules')

def GetTeamSchedule( team, team_schedule ):
    print_str = ""
    for i, round_schedule in enumerate(team_schedule):
        print_str += f"Round {i+1: >2}: "
        if len(round_schedule) < 1:
            print_str += "break\n"
        else:
            court, match_ = round_schedule[0]
            team_index = match_.index(team)
            opponent = match_[~team_index]
            print_str += f"{CourtFormat(court): <28} vs {opponent}\n"
    return print_str

def PrintAllTeamSchedules( team_schedules ):
    for team, team_schedule in team_schedules.items():
        print(f"{' '+team+' ':=^20s}")
        print(GetTeamSchedule(team, team_schedule))
        print('')

def ExtractTeamSchedule(team, schedule):
    rtn = [[] for i in range(len(schedule))]
    for round_i, round_matches in enumerate(schedule.values()):
        for court, match_ in round_matches.items():
            if match_ is not None and team in match_:
                rtn[round_i].append((court, match_))
    return rtn

def PickPopIndex( elems, veto=[], indices=None ):
    # Manipulate a list of indices rather than the full list to preserve
    # index of 'elems' list after popping from list copies
    if indices is None: indices = [i for i,_ in enumerate(elems)]
    # base case
    if len(indices) < 1: return None 
    # pick a random index
    rand_index = random.randint(0, len(indices)-1)
    # check if a team in the veto list is in the selected match
    selected_match = elems[indices[rand_index]]
    overlap = set(veto) & set(selected_match)
    if len(overlap) > 0:
        # we have a clash: recurse to try again
        reduced_indices = indices.copy()
        reduced_indices.pop(rand_index)
        return PickPopIndex( elems, veto, reduced_indices )
    # else: no clash, use this index
    return indices[rand_index]

def PopRandomListElem( elems, veto=[] ):
    pop_index = PickPopIndex(elems, veto)
    if pop_index is None: return None
    return elems.pop(pop_index)

def PopUniqueMatches( two_sets_matches, n_matches ):
    # two_sets_matches tuple of BR_matches and SR_matches remaining
    # n_matches tuple specifying how many BR matches and how many SR matches to pop
    matches = []
    veto = []
    # function to return the list to be popped from at any point:
    def MatchList():
        if len(matches) >= n_matches[0]:
            return two_sets_matches[1]
        return two_sets_matches[0]
    # Loop through the number of required matches and use the pop functions to pull from the
    # relevant list
    for i in range(sum(n_matches)):
        # pop match
        match_ = PopRandomListElem( MatchList(), veto )
        # update veto
        if match_ is not None:
            for team in match_: veto.append(team)
        # save the popped match
        matches.append(match_)
    return matches

def GenerateSchedule( BR_matches, SR_matches ):
    schedule = {}
    for i in range(7):
        m1, m2, m3 = PopUniqueMatches( (BR_matches, SR_matches), (2,1) )
        schedule[f'Round {i+1}'] = {
            'Court 1 (BR)': m1,
            'Court 2 (BR)': m2,
            'Court 3 (SR)': m3
        }

    for i in range(7):
        m1, m2, m3 = PopUniqueMatches( (BR_matches, SR_matches), (1,2) )
        schedule[f'Round {i+8}'] = {
            'Court 1 (BR)': m1,
            'Court 2 (SR)': m2,
            'Court 3 (SR)': m3
        }
    if len(BR_matches) + len(SR_matches) > 0:
        # clashes have meant the schedule hasn't been filled, raise an error
        raise RuntimeError("Random allocation has left unallocated matches due to clashes. Run again.")
    return schedule

def EnergyLoss( team_frequency ):
    # measure for how tiring a schedule would be on a team. Multiple games in a row
    # are punished by increasing the energy spend of adjacent games. Sufficient break
    # will reduce the energy gradient back to 1
    energy_spent = 0
    energy_gradient = 1
    for game in team_frequency:
        if game:
            energy_spent += energy_gradient
            energy_gradient += 3
        else:
            energy_gradient = max(energy_gradient-4, 1)
    return energy_spent

def TotalLoss( team_frequencies ):
    loss_list = [ EnergyLoss(freq) for freq in team_frequencies.values() ]
    return (sum([ loss**2 for loss in loss_list ]), loss_list)


test_energies = [
    [1,0,1,0,1,0,1,0,1,0], # ideal
    [0,1,0,1,0,1,0,1,0,1], # the same
    [1,1,0,0,1,1,0,0,1,0], # a little worse, but good
    [0,1,1,1,0,0,0,1,0,1], # worse
    [0,1,1,1,0,0,1,0,1,0], # a little worse again (perhaps negligible)
    [1,1,1,1,0,0,0,0,0,1], # very bad
    [0,0,0,0,0,1,1,1,1,1]  # worst case
]
