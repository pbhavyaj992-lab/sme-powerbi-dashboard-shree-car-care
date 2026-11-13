# Power BI setup — Shree Car Care, Anand

Sample data only. You need Power BI Desktop. The free version is enough for this. Time: under 2 hours if you follow the steps in order.

## What you need first

- Power BI Desktop installed on Windows
- This folder, with the four CSVs in `data/`
- Nothing else. No database, no paid licence

## 1. Load the data — 15 minutes

1. Open Power BI Desktop. Start with a blank report.
2. Home > Get Data > Text/CSV.
3. Load `data/sample_bookings.csv`.
4. Do the same for `sample_customers.csv`, `sample_services.csv` and `sample_expenses.csv`.
5. In Power Query, check each file once:
   - `booking_date`, `first_visit_date` and `expense_date` should be Date type, not Text.
   - `amount_inr` and `price_inr` should be Whole Number.
   - `phone` should stay as Text. Do not change it to a number or you will lose the leading digit formatting and the blank values.
6. Close and Apply.

You should see: Bookings 320 rows, Customers 185 rows, Services 8 rows, Expenses 54 rows.

If a file loads with 321 rows, you probably counted the header. Check the row count in the status bar, not by counting in Excel.

## 2. Make the Calendar table — 10 minutes

1. Go to Modelling > New Table.
2. Paste the Calendar DAX from `docs/dax_measures.md`.
3. Mark it as a date table: right-click the table > Mark as date table > pick the date column.
4. Add a Month sort column if the months sort A-Z. In the Calendar table, sort `Month` by `MonthNo`.

## 3. Build the model — 15 minutes

1. Go to Model view.
2. Make these relationships, all one-to-many, single direction:
   - `Customers[customer_id]` → `Bookings[customer_id]`
   - `Services[service_id]` → `Bookings[service_id]`
   - `Calendar[date]` → `Bookings[booking_date]`
   - `Calendar[date]` → `Expenses[expense_date]`
3. Do not connect Expenses to Bookings. They are both fact tables. They only meet through Calendar.
4. Hide the ID columns you do not want to show in visuals: `Bookings[customer_id]` and `Bookings[service_id]` can stay hidden in Report view. Keep them for the model only.

See `docs/dax_measures.md` for the full star schema note.

## 4. Add the measures — 20 minutes

1. In Report view, Home > Enter Data. Make a one-column table called `Measures` and delete the dummy row. Or right-click in the Fields pane and make a new table with `Measures = {1}` and hide the column. Either way works.
2. Select the `Measures` table.
3. Add the measures one by one from `docs/dax_measures.md`: Total Revenue, Total Bookings, Completed Bookings, Cancellation Rate, No-Show Rate, Average Bill Value, Repeat Customer %, Total Expenses, Net Cash.
4. Format them:
   - Money measures: Currency, INR, 0 decimal places.
   - Cancellation Rate, No-Show Rate, Repeat Customer %: Percentage, 1 decimal place.
5. Test each one in a card visual before you build pages. Total Revenue should be ₹5,63,201 with no slicer selected. Net Cash should be ₹1,08,541. If it is not, stop and fix the measure. Do not build pages on a wrong number.

## 5. Build the 3 pages — 45 minutes

Follow the layout in `docs/dax_measures.md`. Build in this order:

**Page 1 — Owner overview**
Cards at the top, line chart for revenue by month, bar chart for revenue by service, donut for revenue by channel. Add Month, Channel and Payment Method slicers.

**Page 2 — Services & staff**
Table by service, bar chart by staff, bar chart by service category, Repeat Customer % card.

**Page 3 — Cash**
Cards for revenue, expenses and net cash, column chart for expenses by category, line chart for revenue vs expenses by month, donut for payment method.

Keep the colours simple. One dark colour for the main bars, one light colour for the second series. Do not use a different colour for every bar. The owner should read it, not admire it.

Give every page a clear title. Give every chart a title that says what it shows. For example: "Revenue by service, Jan–Jun 2026 (sample)".

## 6. Check it and export — 15 minutes

1. Click through every slicer once and watch the cards. The numbers should move, but they should never go blank or show an error.
2. Check the totals with no slicer selected against `data/data_notes.md`.
3. File > Export > Export to PDF.
4. Open the PDF and read it. If a title is cut off, or a table runs off the page, fix the report and export again.
5. Save the report as `shree-car-care-dashboard.pbix` in this project folder, next to `README.md`. Do not commit the `.pbix` to GitHub if it gets over 25 MB. A screenshot and the PDF are enough for a portfolio.

## If something looks wrong

| Problem | Likely cause |
|---|---|
| Revenue is much higher than ₹5,63,201 | Your Total Revenue measure is counting cancelled bookings, or the Expenses table is joined to Bookings |
| Revenue by month is blank | Calendar is not marked as a date table, or the relationship to Bookings is the wrong way |
| Customer count looks wrong | You counted rows in Customers (185) instead of customers with a completed booking (146) |
| Repeat Customer % is over 100% | The FILTER / SUMMARIZE in that measure is wrong — copy it again from `dax_measures.md` |
| Amounts show as text | In Power Query, change `amount_inr` to Whole Number and reload |

## Done

When the PDF reads cleanly and the totals match, you have a finished sample project. Put a screenshot in the README only after you have built it. Do not claim this shop is real.
