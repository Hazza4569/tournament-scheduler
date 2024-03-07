import pickle
import schedule as sched

with open('schedules/pickle/loss7507.pkl', 'rb') as f:
    schedule = sched.Schedule(pickle.load(f))

# swap courts 1 and 2 in the 2nd half
for i, (round_, courts) in enumerate(schedule.items()):
    if i >= 7:
        new_courts = {}
        new_courts['Court 1 (SR)'] = courts.pop('Court 2 (SR)')
        new_courts['Court 2 (BR)'] = courts.pop('Court 1 (BR)')
        new_courts['Court 3 (SR)'] = courts.pop('Court 3 (SR)')
        schedule[round_] = new_courts

print(schedule)


from main import teams
import csv, os

loss=7507
try: os.mkdir(f'schedules/csv/loss{loss}/')
except: pass
with open(f'schedules/csv/loss{loss}/full.csv', 'w') as f:
    writer = csv.writer(f)
    court_titles = ['Court 1 (Birmingham rules)', 'Court 2 (Birmingham rules)', 'Court 3 (Sheffield rules)']
    writer.writerow(['']+[ x for ttl in court_titles for x in [ttl, '', ''] ])
    for i, (round_, court_spec) in enumerate(schedule.items()):
        if i == 7:
            # (change court titles)
            court_titles[0] = 'Court 1 (Sheffield rules)'
            writer.writerow([])
            writer.writerow(['']+[ x for ttl in court_titles for x in [ttl, '', ''] ])
        row = [round_]# + [team for match_ in court_spec.values() for team in (match_ if match_ is not None else ['blank','blank'])]
        for match_ in court_spec.values():
            if match_ is None:
                row += ['blank','vs','blank']
            else:
                row += [match_[0], 'vs', match_[1]]
        writer.writerow(row)

for team, team_schedule in schedule.GetTeamSchedules(teams).items():
    with open(f"schedules/csv/loss{loss}/{team.replace(' ','_')}.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow([f"{team} schedule"])
        writer.writerow(["Round","Court","Rules","Opponent"])
        for i, round_schedule in enumerate(team_schedule):
            row = [f"Round {i+1}"]
            if len(round_schedule) < 1:
                for val in ['break','-','-']: row.append(val)
            else:
                court, match_ = round_schedule[0]
                team_index = match_.index(team)
                opponent = match_[~team_index]
                court_no, rules = court.split('(')
                row.append(court_no.strip())
                row.append("Birmingham" if rules[0] == "B" else "Sheffield")
                row.append(opponent)
            writer.writerow(row)
