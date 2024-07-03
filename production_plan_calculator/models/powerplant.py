from typing import Any, Dict

from production_plan_calculator.consts import PowerplantTypes
from production_plan_calculator.exceptions import UnsupportedPowerplantTypeException


class PowerPlant:
    def __init__(
        self,
        name: str,
        type: str,
        efficiency: float,
        pmin: int,
        pmax: int
    ) -> None:
        self.name = name
        self.type = type
        self.efficiency = efficiency
        self.pmin = pmin
        self.pmax = pmax

    def calculate_cost(self, fuels: Dict[str, Any]) -> None:
        if self.type == PowerplantTypes.GAS.value:
            self.cost = fuels["gas(euro/MWh)"] / self.efficiency
        elif self.type == PowerplantTypes.TURBOJET.value:
            self.cost = fuels["kerosine(euro/MWh)"] / self.efficiency
        elif self.type == PowerplantTypes.WIND.value:
            self.cost = 0
        else:
            raise UnsupportedPowerplantTypeException(
                f"This type of powerplant ({self.type}) is not supported."
            )

    def get_pmax(self, wind_percentage: int):
        if self.type == PowerplantTypes.GAS.value:
            return self.pmax
        elif self.type == PowerplantTypes.TURBOJET.value:
            return self.pmax
        elif self.type == PowerplantTypes.WIND.value:
            return (self.pmax * wind_percentage) / 100
        else:
            raise UnsupportedPowerplantTypeException(
                f"This type of powerplant ({self.type}) is not supported."
            )
