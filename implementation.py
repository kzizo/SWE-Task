from abc import ABC
from datetime import datetime, timedelta
from itertools import count

_appointment_ids = count(1)


class User(ABC):
    def __init__(self, userId, name, email):
        self.userId = userId
        self.name = name
        self.email = email
        self._registered = False
        self._loggedIn = False

    def register(self):
        self._registered = True

    def login(self):
        if not self._registered:
            raise ValueError("User must register before logging in.")
        self._loggedIn = True


class TimeSlot:
    def __init__(self, slotId, startTime):
        self.slotId = slotId
        self.startTime = startTime
        self.isBooked = False


class Appointment:
    BOOKED, CANCELLED, COMPLETED = "BOOKED", "CANCELLED", "COMPLETED"

    def __init__(self, patient, doctor, slot):
        self.appointmentId = next(_appointment_ids)
        self.status = Appointment.BOOKED
        self.patient = patient
        self.doctor = doctor
        self.slot = slot

    def cancel(self):
        if self.status != Appointment.BOOKED:
            raise ValueError("Only a booked appointment can be cancelled.")
        if self.slot.startTime <= datetime.now():
            raise ValueError("Cannot cancel an appointment that already started.")
        self.status = Appointment.CANCELLED
        self.slot.isBooked = False

    def complete(self):
        if self.status != Appointment.BOOKED:
            raise ValueError("Only a booked appointment can be completed.")
        self.status = Appointment.COMPLETED


class Doctor(User):
    _directory = []  # every Doctor created, used by Patient.searchDoctors

    def __init__(self, userId, name, email, specialty):
        super().__init__(userId, name, email)
        self.specialty = specialty
        self.slots = []         # Doctor publishes 0..* TimeSlots
        self.appointments = []  # Doctor attends 0..* Appointments
        Doctor._directory.append(self)

    def publishSlot(self, slot):
        if slot not in self.slots:
            self.slots.append(slot)

    def viewDailySchedule(self, date):
        return [a for a in self.appointments
                if a.slot.startTime.date() == date and a.status == Appointment.BOOKED]

    def markCompleted(self, appointment):
        if appointment not in self.appointments:
            raise ValueError("Unknown appointment for this doctor.")
        appointment.complete()


class ClinicSystem:
    MAX_ACTIVE = 3

    def countActive(self, patient):
        now = datetime.now()
        return sum(1 for a in patient.appointments
                   if a.status == Appointment.BOOKED and a.slot.startTime > now)

    def validateBooking(self, patient):
        return self.countActive(patient) < ClinicSystem.MAX_ACTIVE


class Patient(User):
    def __init__(self, userId, name, email, clinic):
        super().__init__(userId, name, email)
        self.clinic = clinic
        self.appointments = []  # Patient owns its Appointments (1 to 0..*)

    def searchDoctors(self, specialty):
        return [d for d in Doctor._directory if d.specialty == specialty]

    def viewSchedule(self, doctor):
        if doctor not in Doctor._directory:
            raise ValueError("Unknown doctor.")
        return [s for s in doctor.slots if not s.isBooked]

    def bookAppointment(self, slot):
        doctor = next((d for d in Doctor._directory if slot in d.slots), None)
        if doctor is None:
            raise ValueError("Unknown time slot.")
        if not self.clinic.validateBooking(self):
            raise ValueError(
                f"Maximum appointment limit reached (N = {ClinicSystem.MAX_ACTIVE}).")
        if slot.isBooked:
            raise ValueError("Slot is no longer available.")
        appointment = Appointment(self, doctor, slot)
        self.appointments.append(appointment)
        doctor.appointments.append(appointment)
        slot.isBooked = True
        return appointment

    def cancelAppointment(self, appointment):
        if appointment not in self.appointments:
            raise ValueError("Unknown appointment for this patient.")
        appointment.cancel()


def main():
    clinic = ClinicSystem()
    doctor = Doctor(1, "Dr. Salma", "salma@clinic.com", "Cardiology")
    patient = Patient(2, "Omar", "omar@mail.com", clinic)
    doctor.register()
    patient.register()
    patient.login()

    base = datetime.now() + timedelta(days=1)
    for i in range(1, 5):
        doctor.publishSlot(TimeSlot(i, base + timedelta(hours=i)))
    slots = patient.viewSchedule(patient.searchDoctors("Cardiology")[0])

    # One successful booking
    appt = patient.bookAppointment(slots[0])
    print(f"Booking 1: status={appt.status}, "
          f"total active={clinic.countActive(patient)}/{ClinicSystem.MAX_ACTIVE}")

    # Fill the limit (setup, not printed)
    patient.bookAppointment(slots[1])
    patient.bookAppointment(slots[2])

    # One rejected booking
    try:
        patient.bookAppointment(slots[3])
    except ValueError as err:
        print(f"Booking 2: status=REJECTED ({err}), "
              f"total active={clinic.countActive(patient)}/{ClinicSystem.MAX_ACTIVE}")


if __name__ == "__main__":
    main()