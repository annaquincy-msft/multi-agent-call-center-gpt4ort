from typing import Annotated
from semantic_kernel.functions import kernel_function
from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os
import json

# Database setup
Base = declarative_base()
sqlite_db_path = os.environ.get("SQLITE_DB_PATH", "../data/sample_patients_db.db")
engine = create_engine(f"sqlite:///{sqlite_db_path}")
Session = sessionmaker(bind=engine)
session = Session()

# Models
class Patient(Base):
    __tablename__ = "patients"
    id = Column(String, primary_key=True)  # <- this exists, and it's TEXT
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    date_of_birth = Column(String)
    address = Column(String)
    zip = Column(String)
    order_status = Column(String)
    action = Column(String)

Base.metadata.create_all(engine)

# Kernel Functions Plugin
class General_Tools:
    @kernel_function(
        name="get_patient_info",
        description="Look up patient details using name and zip code."
    )
    async def get_patient_info(
        self,
        phone_number : Annotated[str, "Patient's phone number"] = None,
        birth_date  : Annotated[str, "Patient's date of birth"] = None,
        zip : Annotated[str, "Patient's zip code"] = None,
    ) -> dict | str:
        try:
            # Normalize the input
            patient = session.query(Patient).filter(
                or_(
                    Patient.phone_number == phone_number,
                    Patient.date_of_birth == birth_date,
                    Patient.zip == zip
                )
            ).first()

            results = []

            if patient:
                matches = {
                    'phone_number': patient.phone_number == phone_number,
                    'date_of_birth': patient.date_of_birth == birth_date,
                    'zip': patient.zip == zip
            }
                
                matched_fields = [k for k, v in matches.items() if v]
                unmatched_fields = [k for k, v in matches.items() if not v]

                if len(matched_fields) == 3:
                        match_type = 'all elelments matched, confirmation completed'
                elif len(matched_fields) == 0:
                    match_type = 'none_matched, ask for confirmation'
                else:
                    match_type = 'some elelments matched, ask for confirmation'               

                print(f"Patient found: {patient.first_name} {patient.last_name}, Zip: {patient.zip}")
            
                return json.dumps({
                    "match_type": match_type,
                    "patient_id": patient.id,
                    "first_name": patient.first_name,
                    "last_name": patient.last_name,
                    "phone_number": patient.phone_number,
                    "date_of_birth": patient.date_of_birth,
                    "address": patient.address,
                    "zip": patient.zip,
                    "order_status": patient.order_status,
                    "action": patient.action
                })
            else:
                print(f"No patient found with name: {phone_number} {birth_date} and zip: {zip}")
                return "Patient not found with the provided information."
        except Exception as e:
            print(f"Error occurred while querying the database: {str(e)}")
            return f"Database error: {str(e)}"

    @kernel_function(
        name="escalate_to_human",
        description="Escalate the conversation to a human agent if the patient declines authorization or requests human support"
    )
    async def escalate_to_human(
        self,
        reason: Annotated[str, "Reason for escalation"] = None,
    ) -> str:
        
        # Create timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format log entry
        log_entry = (
            f"=== Escalation ===\n"
            f"Time: {timestamp}\n"
            f"Reason: {reason}\n"
            f"{'-'*40}\n"
        )

        # Ensure folder exists
        folder = "escalation_logs"
        os.makedirs(folder, exist_ok=True)

        # Save to file
        filename = f"escalation_{datetime.now().isoformat(timespec='minutes').replace(':', '-')}.txt"
        with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
            f.write(reason)
        
        # This is a stub. Replace with a real escalation handler if needed.
        return json.dumps({
            "status": "escalated",
            "reason": reason,
            "message": "A human representative will reach out to you shortly."
        })
