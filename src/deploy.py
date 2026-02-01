from main import air_quality_global_flow 
from prefect.client.schemas.schedules import IntervalSchedule
from datetime import timedelta
if __name__ == "__main__":
    air_quality_global_flow.serve(
        name="aire-prediccion-deployment",
        schedule=IntervalSchedule(interval=timedelta(minutes=30)),
        tags=["servicio-social", "skilliket"] 
    )