# Benchball Varsity Tournament Scheduler

A Python program to help with planning a benchball tournament. The tournament
will involve 10 teams playing across two round-robin groups, where each team
plays all other teams in the group twice (playing a slightly rule variant in
each of the two fixtures).  Scheduling these games needs to consider which
court will be set up for the relevant rule variant, and each team should get a
reasonable timetable with relatively well-placed rests.

This last point is the tricky part, and is handled in this code by first
establishing a loss function which should be minimised, this is a crude
estimate of the energy expended by a team having to play back-to-back games. By
minimising the energy expenditure across all teams, hopefully a balanced
schedule is achieved. This code uses no formal minimisation, but a brute-force
Monte Carlo approach of randomising the schedule many times and finding the
version with the lowest loss function. This approach is quite crude but fairly
effective.

An interesting extension to this would be to train a neural network to generate
schedules which minimise the loss function. For now I decided this was too big
a time investment for a relatively unimportant task.

The code is a bit of a mess currently as I initially wrote it procedurally and
then switched to an object oriented approach partway through.  I didn't fully
clean up the procedural code and for now have stopped at a fully working
version as the result was achieved.  More documentation is definitely also
needed.
