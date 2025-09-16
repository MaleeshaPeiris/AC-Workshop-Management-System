from dataclasses import dataclass

@dataclass
class Job:
    client_name: str
    phone: str
    job_date: str
    is_service: int
    is_repair: int
    service_by: str
    repair_by: str
    next_service_date: str
    notes: str
    job_type: str
    plate: str
    make: str
    model: str
    total_amount: int
