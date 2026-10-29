# Use Cases Specification

## Use Case 1: Book Appointment (Primary Actor: Patient)
- **Description:** Patient books an appointment with a doctor.
- **Main Flow:**
  1. Patient searches for a doctor by specialty.
  2. Patient selects an available appointment slot.
  3. System checks if active upcoming appointments < N (where N = 3).
  4. System confirms booking and updates slot status.
- **Alternative Flow (Limit Exceeded):**
  - At step 3, if Patient already has 3 active upcoming appointments:
    - System rejects the booking request and displays an error message: *"Maximum appointment limit reached (N = 3)."*

## Use Case 2: Manage Schedule (Primary Actor: Doctor)
- **Description:** Doctor sets up and publishes available time slots for booking.
- **Main Flow:**
  1. Doctor logs into the system.
  2. Doctor creates new appointment slots with dates and times.
  3. System saves slots as available for patient search.

---

## Use Case Diagram

```mermaid
graph TD
    Patient((Patient))
    Doctor((Doctor))

    subgraph Clinic System
        UC1[Book Appointment]
        UC2[Cancel Appointment]
        UC3[Manage Schedule]
        UC4[Mark Appointment Completed]
    end

    Patient --> UC1
    Patient --> UC2
    Doctor --> UC3
    Doctor --> UC4
