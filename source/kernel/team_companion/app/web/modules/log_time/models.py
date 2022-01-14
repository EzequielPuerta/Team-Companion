from dataclasses import dataclass

@dataclass
class LogTime():
    def __init__(self, raw_json):
        self.username = raw_json["username"]
        self.display_name = raw_json["displayName"]
        self.period = raw_json["period"]
        self.hours_per_day = raw_json["hoursPerDay"]
        self.worked_redmine = raw_json["workedRedmine"]
        self.worked = raw_json["worked"]
        self.required = raw_json["required"]
        self.required_period = raw_json["requiredPeriod"]

    def __str__(self):
        return f"El usuario {self.username} cargó {self.worked} horas en el período {self.period}."
    
    def __repr__(self):
        return self.__str__()