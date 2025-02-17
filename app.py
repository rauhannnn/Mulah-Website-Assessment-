from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load the CSV file
def load_data():
    df = pd.read_csv("Table_Input.csv")
    df.columns = df.columns.str.strip()  # Remove any accidental spaces
    return df

@app.route('/')
def index():
    df = load_data()
    values_dict = pd.Series(df["Value"].values, index=df["Index #"]).to_dict()
    
    # Compute Table 2 values
    try:
        table_2 = {
            "Alpha": values_dict["A5"] + values_dict["A20"],
            "Beta": values_dict["A15"] / values_dict["A7"],
            "Charlie": values_dict["A13"] * values_dict["A12"]
        }
    except KeyError as e:
        table_2 = {"Error": f"Missing key in data: {str(e)}"}
    
    # Convert DataFrame to properly formatted HTML table without index column
    table_1_html = df.to_html(classes='table table-bordered table1', index=False, header=True)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Table Display</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            .table1 td:first-child, .table1 th:first-child {{
                text-align: left !important; /* Left align Index # column in Table 1 */
            }}
            .table1 th:last-child {{
                text-align: left !important; /* Left align Value header in Table 1 */
            }}
            .table1 td:last-child {{
                text-align: right !important; /* Right align Value column in Table 1 */
            }}
            .table1 th:last-child {{
                text-align: left !important; /* Left align only the Value cell itself */
            }}
            .table2 td, .table2 th {{
                text-align: center !important; /* Center align all cells in Table 2 */
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body class="container mt-5">
        <h2>Table 1</h2>
        <div>{table_1_html}</div>
        <h2>Table 2</h2>
        <table class="table table-bordered table2">
            <tr><th>Category</th><th>Value</th></tr>
            {''.join(f'<tr><td>{key}</td><td>{value}</td></tr>' for key, value in table_2.items())}
        </table>
    </body>
    </html>
    """
    
    return html_content

if __name__ == '__main__':
    app.run(debug=True)
