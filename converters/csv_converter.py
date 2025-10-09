import io
from typing import List

import pandas as pd


class CsvConverter:
    """Converter for CSV files to markdown format."""

    def convert(self, file, include_metadata=True):
        """
        Convert CSV file to markdown.

        Args:
            file: Streamlit uploaded file object
            include_metadata: Whether to include file metadata

        Returns:
            str: Markdown content
        """
        try:
            # Read CSV file
            content = file.read()

            # Try different encodings
            encodings = ["utf-8", "latin-1", "cp1252"]
            df = None

            for encoding in encodings:
                try:
                    csv_content = io.StringIO(content.decode(encoding))
                    df = pd.read_csv(csv_content)
                    break
                except (UnicodeDecodeError, pd.errors.EmptyDataError):
                    continue

            if df is None:
                raise Exception("Could not read CSV file with any supported encoding")

            markdown_lines = []

            # Add metadata if requested
            if include_metadata:
                markdown_lines.extend(self._extract_metadata(df, file.name))
                markdown_lines.append("")

            # Convert DataFrame to markdown table
            markdown_table = self._dataframe_to_markdown(df)
            markdown_lines.extend(markdown_table)

            # Add summary statistics if the data is numeric
            if self._has_numeric_data(df):
                markdown_lines.append("")
                markdown_lines.append("## Summary Statistics")
                markdown_lines.append("")
                summary_table = self._create_summary_table(df)
                markdown_lines.extend(summary_table)

            return "\n".join(markdown_lines)

        except Exception as e:
            raise Exception(f"Error converting CSV file: {str(e)}")

    def _extract_metadata(self, df, filename):
        """Extract CSV metadata."""
        metadata = [
            "---",
            f'title: "{filename}"',
            f'source_format: "CSV"',
            f"rows: {len(df)}",
            f"columns: {len(df.columns)}",
        ]

        # Add column information
        column_types = df.dtypes.to_dict()
        metadata.append("columns:")
        for col, dtype in column_types.items():
            metadata.append(f"  - {col}: {str(dtype)}")

        metadata.append("---")
        return metadata

    def _dataframe_to_markdown(self, df):
        """Convert DataFrame to markdown table format."""
        if df.empty:
            return ["*No data available*"]

        # Limit rows for very large datasets
        display_df = df.head(1000) if len(df) > 1000 else df

        markdown_table = []

        # Create header
        headers = [str(col) for col in display_df.columns]
        markdown_table.append("| " + " | ".join(headers) + " |")
        markdown_table.append("| " + " | ".join(["---"] * len(headers)) + " |")

        # Create data rows
        for _, row in display_df.iterrows():
            cells = []
            for value in row:
                # Clean cell content for markdown
                cell_content = str(value) if pd.notna(value) else ""
                # Escape pipe characters
                cell_content = cell_content.replace("|", "\\|")
                # Limit cell length
                if len(cell_content) > 100:
                    cell_content = cell_content[:97] + "..."
                cells.append(cell_content)

            markdown_table.append("| " + " | ".join(cells) + " |")

        # Add note if data was truncated
        if len(df) > 1000:
            markdown_table.append("")
            markdown_table.append(
                f"*Note: Showing first 1000 rows out of {len(df)} total rows.*"
            )

        return markdown_table

    def _has_numeric_data(self, df):
        """Check if DataFrame has numeric columns."""
        return any(df.select_dtypes(include=["number"]).columns)

    def _create_summary_table(self, df):
        """Create summary statistics table for numeric columns."""
        numeric_df = df.select_dtypes(include=["number"])

        if numeric_df.empty:
            return []

        # Get summary statistics
        summary = numeric_df.describe()

        markdown_table = []

        # Create header
        headers = ["Statistic"] + [str(col) for col in summary.columns]
        markdown_table.append("| " + " | ".join(headers) + " |")
        markdown_table.append("| " + " | ".join(["---"] * len(headers)) + " |")

        # Create rows for each statistic
        for stat in summary.index:
            row_data = [str(stat)]
            for col in summary.columns:
                value = summary.loc[stat, col]
                # Format numbers nicely
                if pd.isna(value):
                    formatted_value = "N/A"
                else:
                    formatted_value = (
                        f"{value:.2f}" if isinstance(value, float) else str(value)
                    )
                row_data.append(formatted_value)

            markdown_table.append("| " + " | ".join(row_data) + " |")

        return markdown_table
