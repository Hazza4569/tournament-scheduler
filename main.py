import random
random.seed(11)
import output
output.random = random
import schedule as sched
## Benchball varsity schedule

# Input: universities and courts
unis = ['Birmingham', 'Exeter', 'Sheffield', 'Bournemouth', 'Chichester']
#teams = [ uni + f" {i+1}" for i in range(2) for uni in unis ]
courts = [ f'Court {i+1}' for i in range(3) ]

# Each uni has 2 teams. All the 1s are in one league and the 2s in another
leagues = [
    [ uni + " 1" for uni in unis],
    [ uni + " 2" for uni in unis]
]
teams = [team for league in leagues for team in league]

# In each league, each team plays every other team once, for each set of rules (birmingham rules (BR) and sheffield rules (SR))
# Get the list of matches between each team and then copy into lists for each set of rules
matches = []
matches = [ [i_team, j_team] for league in leagues for i,i_team in enumerate(league) for j_team in league[i+1:] ]
#BR_matches = matches.copy()
#SR_matches = matches.copy()

if __name__ == "__main__":
    n = 0
    failed_schedules = 0
    best_schedules = {99999999+i: None for i in range(10)}
    while True:
        n+=1
        try:
            #schedule = output.GenerateSchedule(matches.copy(), matches.copy())
            schedule = sched.Schedule.GenerateRandom(matches.copy(), matches.copy(), random)
        except RuntimeError:
            failed_schedules += 1
            continue
        # calculate individual schedules for each team
        team_schedules = schedule.GetTeamSchedules( teams )
        # get match frequencies for analysis
        team_frequencies = { team: [ len(matches) for matches in team_schedule ] for team, team_schedule in team_schedules.items() }
        # check no team is scheduled to play twice in one slot
        if max([n_matches for frequency in team_frequencies.values() for n_matches in frequency]) != 1:
            print("ERROR! A team has scheduling conflicts")
            output.PrintSchedule(schedule)
            output.PrintAllTeamSchedules( team_schedules )
            raise RuntimeError()
        # evaluate loss function given team frequencies
        loss, loss_list = output.TotalLoss( team_frequencies )
        # save if this is a top 10 result
        worst_saved_loss = list(best_schedules)[-1]
        if loss < worst_saved_loss:
            best_schedules.pop(worst_saved_loss)
            best_schedules[loss] = (loss_list, schedule)
            best_schedules = dict(sorted(best_schedules.items()))
        if n>2e6: break

    print(n, failed_schedules)

#ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

    import pickle, os
    for i, (loss, (loss_list, schedule)) in enumerate(best_schedules.items()):
        with open(f'schedules/pickle/loss{loss}.pkl', 'wb') as f:
            pickle.dump(dict(schedule), f)
        try: os.mkdir(f'schedules/txt/loss{loss}/')
        except: pass
        with open(f'schedules/txt/loss{loss}/full.txt', 'w') as f:
            f.write(schedule.__str__())
        with open(f'schedules/txt/loss{loss}/losses.txt', 'w') as f:
            f.write(loss_list.__str__())
        for team, team_schedule in schedule.GetTeamSchedules(teams).items():
            with open(f"schedules/txt/loss{loss}/{team.replace(' ','_')}.txt", 'w') as f:
                f.write(output.GetTeamSchedule(team, team_schedule))
        #print(schedule)
        #output.PrintAllTeamSchedules(team_schedules)

#output.PrintSchedule(schedule)
#output.PrintAllTeamSchedules( team_schedules )


# input to the loss function will be
#freq = [len(matches) for matches in team_schedule]
#immediate failure if
#max(freq) > 1
