# DAX measures and dashboard layout

Business: Shree Car Care, Anand — sample data only, Jan–Jun 2026.

## The model first

Use a star schema. Do not join everything to everything.

- `Bookings` is the fact table.
- `Customers`, `Services` and a `Calendar` table are dimensions.
- `Expenses` is a second fact table, joined to `Calendar` only.

Relationships (both single direction, one-to-many):

- `Customers[customer_id]` → `Bookings[customer_id]`
- `Services[service_id]` → `Bookings[service_id]`
- `Calendar[date]` → `Bookings[booking_date]`
- `Calendar[date]` → `Expenses[expense_date]`

Make a Calendar table in DAX:

```dax
Calendar =
ADDCOLUMNS(
    CALENDAR(DATE(2026, 1, 1), DATE(2026, 6, 30)),
    "Year", YEAR([Date]),
    "Month", FORMAT([Date], "mmm yyyy"),
    "MonthNo", MONTH([Date]),
    "MonthYear", FORMAT([Date], "yyyy-mm")
)
```

Rename the date column to `date` if your version names it differently, and mark it as a date table.

## Measures

Put all of these in a measure table called `Measures`. Do not put them inside the Bookings table.

### Total Revenue

Only completed bookings count. Cancelled and no-show are 0 anyway, but say it clearly in the measure so no one counts them by mistake.

```dax
Total Revenue =
CALCULATE(
    SUM(Bookings[amount_inr]),
    Bookings[status] = "Completed"
)
```

Sample total: ₹5,63,201.

### Total Bookings

```dax
Total Bookings =
COUNTROWS(Bookings)
```

Sample total: 320.

### Completed Bookings

```dax
Completed Bookings =
CALCULATE(
    COUNTROWS(Bookings),
    Bookings[status] = "Completed"
)
```

Sample total: 299.

### Cancellation Rate

Cancelled bookings divided by all bookings. No-show is kept separate.

```dax
Cancellation Rate =
DIVIDE(
    CALCULATE(COUNTROWS(Bookings), Bookings[status] = "Cancelled"),
    [Total Bookings]
)
```

Sample: 12 / 320 = 3.8%. Format as % with 1 decimal.

### No-Show Rate

Same idea, for the owner to see both problems separately.

```dax
No-Show Rate =
DIVIDE(
    CALCULATE(COUNTROWS(Bookings), Bookings[status] = "No-Show"),
    [Total Bookings]
)
```

Sample: 9 / 320 = 2.8%.

### Average Bill Value

Revenue divided by completed bookings only. Do not divide by all 320 bookings, or the average drops for the wrong reason.

```dax
Average Bill Value =
DIVIDE([Total Revenue], [Completed Bookings])
```

Sample: ₹5,63,201 / 299 = ₹1,884.

### Repeat Customer %

Customers with more than one completed booking, out of all customers with at least one completed booking.

```dax
Repeat Customer % =
VAR CustomersWithBookings =
    DISTINCTCOUNT(Bookings[customer_id])
VAR RepeatCustomers =
    COUNTROWS(
        FILTER(
            SUMMARIZE(
                FILTER(Bookings, Bookings[status] = "Completed"),
                Bookings[customer_id],
                "BookingCount", COUNTROWS(Bookings)
            ),
            [BookingCount] > 1
        )
    )
RETURN
    DIVIDE(RepeatCustomers, CustomersWithBookings)
```

Sample: 95 repeat customers out of 146 customers with a completed booking = 65.1%. Format as %.

If this feels slow on a bigger file, make it a simpler version first and come back to it. Do not fake the number.

### Total Expenses

```dax
Total Expenses =
SUM(Expenses[amount_inr])
```

Sample total: ₹4,54,660.

### Net Cash

Revenue minus expenses. This is cash left in this sample period, not profit after tax. Do not call it profit in the report.

```dax
Net Cash =
[Total Revenue] - [Total Expenses]
```

Sample: ₹5,63,201 − ₹4,54,660 = ₹1,08,541.

### Revenue by Payment Method (for a card visual, if needed)

```dax
UPI Revenue =
CALCULATE([Total Revenue], Bookings[payment_method] = "UPI")

Cash Revenue =
CALCULATE([Total Revenue], Bookings[payment_method] = "Cash")

Card Revenue =
CALCULATE([Total Revenue], Bookings[payment_method] = "Card")
```

## The 3-page dashboard

Keep it to three pages. The owner should get the answer in 30 seconds.

### Page 1 — Owner overview

Title: "How is the shop doing?"

At the top, 5 cards in one row:

- Total Revenue
- Total Bookings (with Completed Bookings underneath, in small text)
- Average Bill Value
- Cancellation Rate
- Net Cash

Below that:

- Line chart: Total Revenue by month, using Calendar[Month]. Add Total Expenses as a second line if it stays readable.
- Bar chart: Total Revenue by service, sorted high to low.
- Donut: Total Revenue by channel — Walk-in, Instagram, Referral, Google.
- Slicers at the top: Month, Channel, Payment Method.

What the owner should learn here: is money going up or down, and which service is doing the work.

### Page 2 — Services & staff

Title: "Which services and who is doing them?"

- Table: service name, Total Bookings, Completed Bookings, Total Revenue, Average Bill Value. Sort by revenue.
- Bar chart: Completed Bookings by staff name. Add Total Revenue as a tooltip so you can see if someone does many small washes or fewer big coatings.
- Bar chart: Total Revenue by service category — Wash, Detailing, Coating.
- Card: Repeat Customer %.
- Slicers: Month, Service Category, Staff.

What the owner should learn here: which services to push, and whether work is spread across staff or stuck with one person.

Do not use this page to rank staff in public. It is for the owner only.

### Page 3 — Cash

Title: "What came in, what went out?"

- Cards: Total Revenue, Total Expenses, Net Cash.
- Column chart: Total Expenses by category — Rent, Salaries, Materials, Utilities, Marketing, Maintenance, Other.
- Line chart: Total Revenue vs Total Expenses by month.
- Donut: Total Revenue by payment method — UPI, Cash, Card.
- Small table: expenses by month and category, for the owner to check.

What the owner should learn here: cash is not the same as sales. Rent and salaries are fixed every month, so a slow month still costs about the same.

## Checks before you share it

- Pick a month slicer and add the cards up by hand once. Revenue + expenses must still match the totals in `data/data_notes.md`.
- Cancelled bookings must show 0 revenue. If a cancelled booking shows money, your Total Revenue measure is wrong.
- The Repeat Customer % must not go over 100%. If it does, your filter is wrong.
- Save the file, then export to PDF and read the PDF once. If a chart title is cut off in the PDF, fix the report, not the PDF.
