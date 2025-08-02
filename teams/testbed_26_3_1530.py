#remade defense system
#TODO: giant targeting
from teams.helper_function import Troops, Utils

# deployable area: pos[0]: x of -25 to 25 pos[1] y 0 to 25
team_name = "BlueForce2"
# troops = [
#     Troops.balloon,
#     Troops.prince,
#     Troops.wizard, 
#     Troops.dragon,
    #     Troops.valkyrie,
    #     Troops.knight,
    #     Troops.archer,
    #     Troops.skeleton
    # ]
# troops=[]
    #splash troops
troops=[Troops.wizard,Troops.skeleton,Troops.minion,Troops.dragon]
    # troops=[Troops.dragon]
# troops=[Troops.valkyrie]

deploy_list = Troops([])
team_signal = "0"

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal


def logic(arena_data: dict):
    atd=Troops.troops_data

    global team_signal
    my_tower = arena_data["MyTower"]
    opp_tower = arena_data["OppTower"]
    my_troops = arena_data["MyTroops"]
    opp_troops = arena_data["OppTroops"]

    #flag for opponent bulk troops
    bulk_troops = {'Skeleton':False, 'Archer':False,'Minion':False, 'Barbarian':False}
    elixir_available = my_tower.total_elixir
    deployable_troops = my_tower.deployable_troops

    cleaned_opp_troops = []
    for i in range(len(opp_troops)):
        # print('Target',opp_troops[i].name,opp_troops[i].position[0],opp_troops[i].position[1])
        is_unique = True
        for j in range(i+1,len(opp_troops)):
            # print("  match",opp_troops[j].name,opp_troops[j].position[0],opp_troops[j].position[1])
            if opp_troops[i].position[0] == opp_troops[j].position[0] and opp_troops[i].name == opp_troops[j].name and opp_troops[i].position[1] == opp_troops[j].position[1]:
                is_unique = False
                # print("  removed")
                break
        if is_unique:
            cleaned_opp_troops.append(opp_troops[i])
    
    ors=[]
    for i in range(len(cleaned_opp_troops)):
        # print('Target',opp_troops[i].name,opp_troops[i].position[0],opp_troops[i].position[1])
        is_unique = True
        for j in range(i+1,len(cleaned_opp_troops)):
            # print("  match",opp_troops[j].name,opp_troops[j].position[0],opp_troops[j].position[1])
            if abs(cleaned_opp_troops[i].position[0] - cleaned_opp_troops[j].position[0]) < 0.5 and \
               abs(cleaned_opp_troops[i].position[1] - cleaned_opp_troops[j].position[1]) < 0.5 and \
               cleaned_opp_troops[i].name == cleaned_opp_troops[j].name:
                is_unique = False
                # print("  removed")
                break
        if is_unique:
            ors.append(cleaned_opp_troops[i])
    
    specific_defense_taken=False
    for troop in ors:
        specific_defense_taken=defensive_action(troop, deployable_troops, elixir_available, bulk_troops, atd)
        
    
    print('\'')
    print('  \'')

def defensive_action(enemy, deployable_troops, elixir_available,bulk_troops,atd):
    pos = enemy.position
    splash_troops = [Troops.wizard, Troops.dragon, Troops.valkyrie]

    if enemy.name in bulk_troops and (not bulk_troops[enemy.name]) and (enemy.target==None or enemy.target=='Tower 1' or enemy.target=='Tower 2') :
            if 0 <= pos[1] <= 50:
                splash_scores = {'Wizard': 3, 'Dragon': 4, 'Valkyrie': 2}
                if enemy.type == 'air':
                    splash_scores['Valkyrie'] = 0  # Valkyrie cannot counter air troops
                elif enemy.type == 'ground':
                    splash_scores['Valkyrie'] = 5

                # Sort splash troops by score, deploy the highest scoring troop available with sufficient elixir
                splash_troops.sort(key=lambda x: splash_scores[x], reverse=True)
                for troop in splash_troops:
                    if troop in deployable_troops and elixir_available >= atd[troop].elixir and splash_scores[troop] > 0:
                        # print(atd[troop].attack_range)
                        deploy_list.list_.append((troop, (pos[0],max(0, pos[1] - atd[troop].attack_range*2))))
                        # deploy_list.list_.append((troop, (25, 50)))
                        bulk_troops[enemy.name] = True  # Mark this bulk troop as countered
                        print(bulk_troops)
                        return True
    
    tank_troops = ['Giant', 'Knight', 'Prince','Balloon']
    if enemy.name in tank_troops :
        if 0 <= pos[1] <= 25:
            tankbuster_scores={'Skeleton':5,'Minion': 4,'Wizard':3, 'Archer': 2}
            if enemy.type == 'air':
                tankbuster_scores['Skeleton'] = 0

            # Sort tankbuster troops by score, deploy the highest scoring troop available with sufficient elixir
            for troop, score in sorted(tankbuster_scores.items(), key=lambda item: item[1], reverse=True):
                if troop in deployable_troops and elixir_available >= atd[troop].elixir and score>0:
                    deploy_list.list_.append((troop, (pos[0], max(0, pos[1] - atd[troop].attack_range))))
                    return True
                
    if enemy.name=='Wizard':
        if 0 <= pos[1] <= 50:
            if Troops.prince in deployable_troops and elixir_available >= atd['Prince'].elixir:
                deploy_list.list_.append((Troops.Prince, (pos[0], max(0, pos[1] - atd['Prince'].attack_range))))
                return True
    
    if enemy.name=='Valkyrie':
        if 0 <= pos[1] <= 25:
            air_troops_scores = {'Minion': 1, 'Dragon': 3}
            for troop, score in sorted(air_troops_scores.items(), key=lambda item: item[1], reverse=True):
                if troop in deployable_troops and elixir_available >= atd[troop].elixir:
                    deploy_list.list_.append((troop, (pos[0], max(0, pos[1] - atd[troop].attack_range))))
                    return True
        
    if enemy.name == 'Dragon':
        # Match with dragon, minion, wizard, archer in that order
        if 0 <= pos[1] <= 25:
            dragon_scores = {'Dragon': 4, 'Minion': 3, 'Wizard': 2, 'Archer': 1}
            for troop, score in sorted(dragon_scores.items(), key=lambda item: item[1], reverse=True):
                if troop in deployable_troops and elixir_available >= atd[troop].elixir:
                    deploy_list.list_.append((troop, (pos[0], max(0, pos[1] - atd[troop].attack_range))))
                    return True
    # If no specific counter, deploy any available troop that can attack the enemy (NOT Giant/balloon)
    return False
        
    


            
        
    
    # print(enemy.name)
def unspecific_counter(enemy, deployable_troops, elixir_available, atd):
    pos = enemy.position
    for troop in deployable_troops:
        print("####")

        if 0 <= pos[1] <= 25:
            print(enemy)
            print(enemy.name)
            print(enemy.position)   
            if troop not in ['Giant','Balloon']:
                if elixir_available >= atd[troop].elixir and enemy.target==None or enemy.target=='Tower 1' or enemy.target=='Tower 2':
                    if enemy.type == 'air' and atd[troop].type in ['air', 'both']:
                        deploy_list.list_.append((troop, (pos[0], max(0, pos[1] - atd[troop].attack_range))))
                        return
                    elif enemy.type == 'ground' and atd[troop].type in ['ground', 'both']:
                        deploy_list.list_.append((troop, (pos[0], max(0, pos[1] - atd[troop].attack_range))))
                        return


def get_active_troops(my_troops):
    """String describing what types of troops are on the field."""
    names = [t.name for t in my_troops]
    if "Giant" in names:
        return "GW+" if any(n in names for n in ["Wizard", "Valkyrie", "Dragon", "Archer"]) else "GW"
    if "Prince" in names:
        return "PW+" if any(n in names for n in ["Wizard", "Valkyrie", "Dragon", "Archer"]) else "PW"
    return "DF"