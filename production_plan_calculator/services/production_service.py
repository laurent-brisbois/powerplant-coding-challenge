from collections import namedtuple

from production_plan_calculator.exceptions import CouldNotReachExpectedLoadException
from production_plan_calculator.models.powerplant import PowerPlant


PowerPlantProduction = namedtuple('PowerPlantProduction', ["name", "p"])


def get_production_plan(payload):
    powerplants = [
        PowerPlant(**powerplant) for powerplant in payload["powerplants"]
    ]
    for powerplant in powerplants:
        powerplant.calculate_cost(payload["fuels"])

    sorted_powerplants = sorted(powerplants, key=lambda p: p.cost)

    load = payload["load"]
    generated = 0
    plan = []

    for powerplant in sorted_powerplants:
        if generated == load:  # we have enough power
            plan.append(PowerPlantProduction(powerplant.name, 0.0))
            continue
        if powerplant.pmin > load - generated:  # pmin is too big for remaining load
            plan.append(PowerPlantProduction(powerplant.name, 0.0))
            continue

        power = powerplant.get_pmax(wind_percentage=payload["fuels"]["wind(%)"])


        if power > load - generated:  # we can't take power as is
            power = load - generated
        
        plan.append(PowerPlantProduction(powerplant.name, round(power, 1)))
        generated += power

    if generated != load:
        raise CouldNotReachExpectedLoadException(
            f"Couldn't reach expected load of '{load}', but only {generated}"
        )

    return [
        {
            "name": power_plant_production.name,
            "p": power_plant_production.p,
        } for power_plant_production in plan
    ]
