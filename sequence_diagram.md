# Sequence Diagram: Book Appointment

This diagram models Use Case 1 (Book Appointment) from `2_use_cases.md`. It uses the classes, methods and
attributes of the class diagram (`User`, `Patient`, `Doctor`, `ClinicSystem`, `TimeSlot`, `Appointment`) and
the business rule `MAX_ACTIVE = 3` (requirement R4).

```mermaid
sequenceDiagram
    autonumber
    actor U as Patient Actor
    participant Pt as Patient
    participant CS as ClinicSystem
    participant TS as TimeSlot
    participant A as Appointment

    U->>Pt: searchDoctors(specialty)
    Pt-->>U: matching Doctors
    U->>Pt: viewSchedule(doctor)
    Pt-->>U: available TimeSlots
    U->>Pt: bookAppointment(slot)

    Pt->>CS: validateBooking(patient)
    CS->>CS: countActive(patient)
    Note over CS: Compares the count with MAX_ACTIVE = 3

    alt Limit reached (count equals MAX_ACTIVE)
        CS-->>Pt: false
        Pt-->>U: Error - Maximum appointment limit reached (N = 3)
    else Limit not reached
        CS-->>Pt: true
        Pt->>TS: read isBooked
        alt Slot already booked
            TS-->>Pt: isBooked = true
            Pt-->>U: Error - slot is no longer available
        else Slot is free
            TS-->>Pt: isBooked = false
            Pt->>A: create appointment (patient, doctor, slot)
            A-->>Pt: Appointment
            Pt->>TS: set isBooked = true
            Pt-->>U: Booking confirmed
        end
    end
```

## How the diagram maps to the other deliverables

| Diagram element | Source |
|---|---|
| Steps 1-5 (search, view schedule, book) | `Patient.searchDoctors`, `viewSchedule`, `bookAppointment` in the class diagram; Use Case 1, steps 1-2 |
| `validateBooking` / `countActive` | `ClinicSystem` in the class diagram; Use Case 1, step 3; requirement R4 |
| Limit-reached branch | Use Case 1, alternative flow (Limit Exceeded) |
| `isBooked` check, then `isBooked = true` | `TimeSlot.isBooked`; Use Case 1, step 4 ("updates slot status") |
| `Appointment` creation | `Patient` "books" `Appointment` (1 to 0..*) in the class diagram |
