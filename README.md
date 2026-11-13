# Shree Car Care, Anand — Sales Dashboard

Hi. I am Bhavya Patel. I built this as a sample project.

Shree Car Care is not a real client. It is a made-up detailing centre in Anand. I made the data so I could show how a small business can see its sales, services and cash in one place.

The data is sample only. Jan to Jun 2026. 120 days. 320 bookings.

## What is in the numbers

- 320 bookings in total
- 299 completed, 12 cancelled, 9 no-show
- 185 customers in the file, 146 of them had at least one completed booking
- 8 services, from a basic wash to ceramic coating
- Total revenue from completed bookings: ₹5,63,201
- Total expenses in the file: ₹4,54,660
- Net cash: ₹1,08,541
- Average bill for a completed booking: ₹1,884

These are sample numbers. They are not from a real shop.

## Files

```
data/
  sample_bookings.csv     320 rows
  sample_customers.csv    185 rows
  sample_services.csv     8 rows
  sample_expenses.csv     54 rows
  data_notes.md           what I cleaned and what I left as it is

scripts/
  generate_sample_data.py  makes all four CSVs again, same result every time

docs/
  dax_measures.md         the measures and the 3-page layout
  powerbi_setup.md        how to build it in Power BI Desktop
```

## How to use it

1. Open Power BI Desktop.
2. Load the four CSVs from `data/`.
3. Follow `docs/powerbi_setup.md`. It takes under 2 hours.
4. Build the three pages in `docs/dax_measures.md`.

I did not include a `.pbix` file. I built the data and the model. You can build the report in Power BI from that.

## How to make the data again

```bash
python3 scripts/generate_sample_data.py
```

It uses seed 42. So you get the same rows every time. It only uses Python's normal library. No extra packages.

## What I left messy on purpose

Real shop data is never clean. So this file has a few things like that:

- 9 customers have no phone number.
- 12 bookings are cancelled and 9 are no-show. Their amount is 0.
- Some notes have spelling mistakes. Like "custmer" and "ceramik". I kept those in the notes column only. The rest of the file is clean.
- Payment is mostly UPI and cash. Some is card.

I wrote more about this in `data/data_notes.md`.

## What this is for

If you run a small service business, this shows:

- Which services bring in the most money.
- Which months are slow.
- How many customers come back.
- Where the money comes from: walk-in, Instagram, referral or Google.
- What is left after expenses.

That is it. No big claims. Just a clear dashboard for a small shop.
