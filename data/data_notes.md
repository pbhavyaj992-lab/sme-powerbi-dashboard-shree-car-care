# Data notes — Shree Car Care, Anand (sample)

This data is made up. It is for a sample Power BI project only. No real business, no real customers.

Period: Jan to Jun 2026. 120 booking days inside that period.
Generator: `scripts/generate_sample_data.py`, seed 42. Re-run it and you get the same files.

## The files

| File | Rows | What it is |
|---|---|---|
| `sample_bookings.csv` | 320 | One row per booking |
| `sample_customers.csv` | 185 | One row per customer |
| `sample_services.csv` | 8 | Price list |
| `sample_expenses.csv` | 54 | 9 expense types x 6 months |

## Totals I checked after generating

- Bookings: 320 — Completed 299, Cancelled 12, No-Show 9
- Booking dates: 120 distinct days, from 2026-01-01 to 2026-06-30
- Revenue, completed bookings only: ₹5,63,201
- Average bill, completed bookings only: ₹1,884
- Expenses: ₹4,54,660
- Net cash (revenue − expenses): ₹1,08,541
- Customers: 185. 9 have no phone number.
- Customers with at least one completed booking: 146. Of those, 95 had more than one completed booking (65.1% repeat).

## What I cleaned

- Dates are all `YYYY-MM-DD`.
- Service names are the same in every file. No "Foam wash", "foam Wash" and "FOAM WASH" in different rows.
- City names are standard: Anand, Vallabh Vidyanagar, Karamsad, Borsad, Nadiad, Petlad.
- Channel is one of Walk-in, Instagram, Referral or Google. Same list in customers and bookings.
- Payment method is one of UPI, Cash or Card for bookings, and UPI, Cash or Bank Transfer for expenses.
- Cancelled and No-Show bookings have amount 0 and no payment method. That is on purpose — they did not pay.
- Every `customer_id` in bookings exists in customers. Every `service_id` in bookings exists in services. I checked this after generating.

## What I left messy on purpose

Real shop sheets have gaps. So:

- 9 customers have a blank phone. Those are walk-ins where the shop did not take a number.
- The `notes` column has spelling mistakes from a real register, for example "custmer", "ceramik", "durty", "paymnt". I kept those in notes only. I did not let them into service names, dates or amounts.
- Not every customer in the customer file has a booking in this period. 36 of the 185 have no booking here. That happens with older customers.

## Things to know before you use it in Power BI

- `amount_inr` is the price of the service for a completed booking. There is no discount column in this version. If you want discounts, add a column and do not change the price list.
- Expenses are monthly totals per category, not per booking. So do not join expenses to bookings by date and sum both in the same visual. Use the Net Cash measure in `docs/dax_measures.md` instead.
- The centre does not have service data before Jan 2026 or after Jun 2026 in this file. Do not present this as a full-year picture.
- Names and phones are made up. The phone numbers are random 10-digit numbers. Do not call or message them.
