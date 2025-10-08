import re
from typing import List

class TxtConverter:
    """Converter for TXT files to markdown format."""
    
    def convert(self, file, include_metadata=True):
        """
        Convert TXT file to markdown.
        
        Args:
            file: Streamlit uploaded file object
            include_metadata: Whether to include file metadata
            
        Returns:
            str: Markdown content
        """
        try:
            # Read file content with different encodings
            content = self._read_with_encoding(file)
            
            markdown_lines = []
            
            # Add metadata if requested
            if include_metadata:
                markdown_lines.extend(self._extract_metadata(file.name, content))
                markdown_lines.append("")
            
            # Process the content
            processed_content = self._process_text_content(content)
            markdown_lines.extend(processed_content)
            
            return "\n".join(markdown_lines)
            
        except Exception as e:
            raise Exception(f"Error converting TXT file: {str(e)}")
    
    def _read_with_encoding(self, file):
        """Read file content trying different encodings."""
        content = file.read()
        
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
        
        for encoding in encodings:
            try:
                return content.decode(encoding)
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail, use utf-8 with error handling
        return content.decode('utf-8', errors='replace')
    
    def _extract_metadata(self, filename, content):
        """Extract text file metadata."""
        lines = content.split('\n')
        word_count = len(content.split())
        char_count = len(content)
        line_count = len(lines)
        
        metadata = [
            "---",
            f"title: \"{filename}\"",
            f"source_format: \"TXT\"",
            f"lines: {line_count}",
            f"words: {word_count}",
            f"characters: {char_count}",
        ]
        
        # Try to detect if it's a structured format
        structure_type = self._detect_structure(content)
        if structure_type:
            metadata.append(f"structure: \"{structure_type}\"")
        
        metadata.append("---")
        return metadata
    
    def _detect_structure(self, content):
        """Detect if the text has any recognizable structure."""
        lines = content.split('\n')
        
        # Check for markdown-like headers
        header_count = sum(1 for line in lines if re.match(r'^#{1,6}\s+', line.strip()))
        if header_count > 0:
            return "markdown-like"
        
        # Check for numbered lists
        numbered_list_count = sum(1 for line in lines if re.match(r'^\d+\.\s+', line.strip()))
        if numbered_list_count > 2:
            return "numbered-list"
        
        # Check for bullet points
        bullet_count = sum(1 for line in lines if re.match(r'^[-*+]\s+', line.strip()))
        if bullet_count > 2:
            return "bullet-list"
        
        # Check for email-like format
        if re.search(r'^(From|To|Subject|Date):', content, re.MULTILINE | re.IGNORECASE):
            return "email-like"
        
        # Check for code-like structure
        if re.search(r'(function|class|def|import|#include)', content, re.IGNORECASE):
            return "code-like"
        
        return None
    
    def _process_text_content(self, content):
        """Process text content and apply intelligent formatting."""
        lines = content.split('\n')
        processed_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            processed_line = self._process_line(line, i, lines)
            
            if processed_line is not None:
                processed_lines.append(processed_line)
            
            i += 1
        
        return processed_lines
    
    def _process_line(self, line, index, all_lines):
        """Process individual line with context."""
        stripped_line = line.strip()
        
        # Handle empty lines
        if not stripped_line:
            return ""
        
        # Detect and convert headers (lines followed by ===== or -----)
        if index < len(all_lines) - 1:
            next_line = all_lines[index + 1].strip()
            if re.match(r'^=+$', next_line) and len(next_line) >= len(stripped_line) * 0.7:
                return f"# {stripped_line}"
            elif re.match(r'^-+$', next_line) and len(next_line) >= len(stripped_line) * 0.7:
                return f"## {stripped_line}"
        
        # Skip underline markers (they're handled above)
        if re.match(r'^[=-]+$', stripped_line):
            return None
        
        # Detect numbered lists
        if re.match(r'^\d+\.\s+', stripped_line):
            return stripped_line
        
        # Detect bullet points and convert to markdown
        if re.match(r'^[-*+]\s+', stripped_line):
            return stripped_line
        
        # Detect potential headers (ALL CAPS lines that are short)
        if (stripped_line.isupper() and 
            len(stripped_line) < 80 and 
            len(stripped_line.split()) <= 10 and
            not re.search(r'[.!?]$', stripped_line)):
            return f"## {stripped_line.title()}"
        
        # Detect code blocks (lines starting with 4+ spaces or tabs)
        if re.match(r'^    ', line) or re.match(r'^\t', line):
            # Check if we're starting a code block
            if (index == 0 or 
                not (re.match(r'^    ', all_lines[index-1]) or re.match(r'^\t', all_lines[index-1]))):
                return f"```\n{line}"
            # Check if we're ending a code block
            elif (index == len(all_lines) - 1 or 
                  not (re.match(r'^    ', all_lines[index+1]) or re.match(r'^\t', all_lines[index+1]))):
                return f"{line}\n```"
            else:
                return line
        
        # Detect URLs and make them links
        url_pattern = r'(https?://[^\s]+)'
        if re.search(url_pattern, stripped_line):
            processed_line = re.sub(url_pattern, r'[\1](\1)', stripped_line)
            return processed_line
        
        # Detect email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, stripped_line):
            processed_line = re.sub(email_pattern, r'[\g<0>](mailto:\g<0>)', stripped_line)
            return processed_line
        
        # Regular paragraph
        return stripped_line
