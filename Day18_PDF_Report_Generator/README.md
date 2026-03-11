# Day 18: PDF Report Generator

## Project Description

This project demonstrates how to programmatically generate professional PDF reports using Python's `ReportLab` library. The generated reports can include dynamic content such as titles, text paragraphs, data summaries, and charts. This is particularly useful for automating the creation of invoices, sales reports, financial statements, or any document that requires a structured and visually appealing PDF output.

## Features

- **Dynamic Content**: Generate reports with variable titles, dates, and textual content.
- **Data Integration**: Incorporate data summaries directly into the report.
- **Visualizations**: Include bar charts to represent data trends (e.g., sales performance).
- **Page Breaks**: Manage document flow with automatic and manual page breaks.
- **Custom Styling**: Apply custom paragraph styles for headings and body text.

## Installation

To run this project, you need to install the `ReportLab` library. You can install it using pip:

```bash
pip install reportlab
```

## Usage

1. **Run the script**:

   Navigate to the project directory and run the Python script:

   ```bash
   python pdf_report_generator.py
   ```

2. **Customize the report**:

   Modify the `generate_report` function in `pdf_report_generator.py` to change the report title, content, and data. The `sample_data` in the `if __name__ == "__main__":` block can be updated with your own dataset.

   ```python
   sample_data = [
       {'month': 'January', 'sales': 1200, 'profit': 250},
       {'month': 'February', 'sales': 1500, 'profit': 300},
       {'month': 'March', 'sales': 1300, 'profit': 280},
       {'month': 'April', 'sales': 1800, 'profit': 350},
       {'month': 'May', 'sales': 1600, 'profit': 320},
   ]
   generate_report(filename="my_custom_report.pdf", title="My Company's Sales Overview", data=sample_data)
   ```

## Project Structure

```
Day18_PDF_Report_Generator/
├── README.md
└── pdf_report_generator.py
```

## Dependencies

- `reportlab`

## Example Output

A `sales_report.pdf` file will be generated in the same directory as the script, containing the structured report and a bar chart visualizing the sales data.

## Author

Manus AI
