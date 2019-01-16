from django.core.management.base import BaseCommand, CommandError
from ipl_data.models import Matches, Deliveries
from django.db import connection, transaction
import csv


class Command(BaseCommand):
    help = 'Load the data from csv to mysql'

    
    def handle(self, *args, **kwargs):

        matches_reader = csv.DictReader(open('/home/monk/mountblue/ipl-data-set/matches.csv'))
        deliveries_reader = csv.DictReader(open('/home/monk/mountblue/ipl-data-set/deliveries.csv'))

        with transaction.atomic():
            for match in matches_reader:
                matches = Matches(
                            id=match["id"],
                            season=match["season"],
                            city=match["city"],
                            date=match["date"],
                            team1=match["team1"],
                            team2=match["team2"],
                            toss_winner=match["toss_winner"],
                            toss_decision=match["toss_decision"],
                            result=match["result"],
                            dl_applied=match["dl_applied"],
                            winner=match["winner"],
                            win_by_runs=match["win_by_runs"],
                            win_by_wickets=match["win_by_wickets"],
                            player_of_match=match["player_of_match"],
                            venue=match["venue"],
                            umpire1=match["umpire1"],
                            umpire2=match["umpire2"],
                            umpire3=match["umpire3"]
                            )
                matches.save()       

        with transaction.atomic():
            for delivery in deliveries_reader:
                deliveries = Deliveries(
                                match = Matches.objects.get(id=delivery['match_id']),            
                                inning=delivery['inning'],
                                batting_team=delivery['batting_team'],
                                bowling_team=delivery['bowling_team'],
                                over=delivery['over'],
                                ball=delivery['ball'],
                                batsman=delivery['batsman'],
                                non_striker=delivery['non_striker'],
                                bowler=delivery['bowler'],
                                is_super_over=delivery['is_super_over'],
                                wide_runs=delivery['wide_runs'],
                                bye_runs=delivery['bye_runs'],
                                legbye_runs=delivery['legbye_runs'],
                                noball_runs=delivery['noball_runs'],
                                penalty_runs=delivery['penalty_runs'],
                                batsman_runs=delivery['batsman_runs'],
                                extra_runs=delivery['extra_runs'],
                                total_runs=delivery['total_runs'],
                                player_dismissed=delivery['player_dismissed'],
                                dismissal_kind=delivery['dismissal_kind'],
                                fielder=delivery['fielder']
                )
                deliveries.save()
            # cursor = connection.cursor()

            # result = cursor.execute("LOAD DATA LOCAL INFILE '/home/monk/mountblue/ipl-data-set/matches.csv' INTO TABLE ipl_data_matches FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 LINES;")

            # print(result)


            # result = cursor.execute("LOAD DATA LOCAL INFILE '/home/monk/mountblue/ipl-data-set/deliveries.csv' INTO TABLE ipl_data_deliveries FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES ( match_id ,inning, batting_team, bowling_team, over, ball, batsman, non_striker, bowler, is_super_over, wide_runs, bye_runs, legbye_runs, noball_runs, penalty_runs, batsman_runs, extra_runs, total_runs, player_dismissed, dismissal_kind, fielder);")  

            # if result:
            #     print(result)

