ACCOUNT_TEMPLATE = "<span><h4>{name}:</h4> ${balance} <em>({updated})</em></span><br />"

TRANSACTION_TABLE = """
<table>
    <tr>
        <th>Payee</th>
        <th>Amount</th>
    </tr>
    {data}
</table>
"""

DAILY_EMAIL = """
<h3>Daily Finance Report: {date}</h3>

<hr />

{data}
"""

WEEKLY_EMAIL = """
<h3>Finances for {dateRange}</h3>

<hr />

{data}
"""
