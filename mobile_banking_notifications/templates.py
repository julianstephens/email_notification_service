ACCOUNT_TEMPLATE = "<span><h4>{name}:</h4> ${balance} <em>({updated})</em></span><br />"

TRANSACTION_TABLE_TEMPLATE = """
<table>
    <tr>
        <th>Payee</th>
        <th>Amount</th>
    </tr>
    {data}
</table>
"""

DAILY_EMAIL_TEMPLATE = """
<html>
    <body>
        <style>
            {styles}
        </style>
        <h3>Daily Finance Report: {date}</h3>

        <hr />

        {data}
    </body>
</html>
"""

WEEKLY_EMAIL_TEMPLATE = """
<html>
    <body>
        <style>
            {styles}
        </style>
        <h3>Finances for {dateRange}</h3>

        <hr />

        {data}
    </body>
</html>
"""
