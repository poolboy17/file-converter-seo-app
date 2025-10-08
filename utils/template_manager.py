from typing import Dict, Any
from datetime import datetime

class TemplateManager:
    """Manage HTML templates and styling options."""
    
    def __init__(self):
        self.templates = {
            'modern': self._modern_template,
            'minimal': self._minimal_template,
            'classic': self._classic_template,
            'dark': self._dark_template
        }
        
        self.color_schemes = {
            'blue': {'primary': '#667eea', 'secondary': '#764ba2', 'text': '#333', 'bg': '#f5f5f5'},
            'green': {'primary': '#11998e', 'secondary': '#38ef7d', 'text': '#333', 'bg': '#f0f9ff'},
            'purple': {'primary': '#8e2de2', 'secondary': '#4a00e0', 'text': '#333', 'bg': '#f5f3ff'},
            'orange': {'primary': '#f46b45', 'secondary': '#eea849', 'text': '#333', 'bg': '#fff7ed'},
            'dark': {'primary': '#2d3748', 'secondary': '#4a5568', 'text': '#e2e8f0', 'bg': '#1a202c'}
        }
    
    def generate_html(self, content: str, title: str, template: str = 'modern', 
                     color_scheme: str = 'blue', font_family: str = None) -> str:
        """
        Generate HTML with selected template and styling.
        
        Args:
            content: Markdown-converted HTML content
            title: Page title
            template: Template name
            color_scheme: Color scheme name
            font_family: Optional custom font family
            
        Returns:
            str: Complete HTML document
        """
        colors = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        
        if template in self.templates:
            return self.templates[template](content, title, colors, font_family)
        else:
            return self.templates['modern'](content, title, colors, font_family)
    
    def _modern_template(self, content: str, title: str, colors: Dict[str, str], font: str = None) -> str:
        """Modern gradient template."""
        font_family = font or '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: {font_family};
            line-height: 1.6;
            color: {colors['text']};
            background: {colors['bg']};
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            color: white;
            padding: 3rem 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .meta {{
            opacity: 0.9;
            font-size: 0.95rem;
        }}
        
        main {{
            background: white;
            margin: 2rem auto;
            padding: 3rem;
            border-radius: 12px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.05);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: {colors['primary']};
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        
        h1 {{
            font-size: 2.5rem;
            border-bottom: 3px solid {colors['primary']};
            padding-bottom: 0.5rem;
        }}
        
        h2 {{
            font-size: 2rem;
            border-bottom: 2px solid {colors['secondary']};
            padding-bottom: 0.3rem;
        }}
        
        a {{
            color: {colors['primary']};
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        a:hover {{
            color: {colors['secondary']};
            text-decoration: underline;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        th {{
            background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
            color: white;
            font-weight: 600;
        }}
        
        tr:hover {{
            background-color: rgba(102, 126, 234, 0.05);
        }}
        
        code {{
            background-color: #f7fafc;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-size: 85%;
            border: 1px solid #e2e8f0;
        }}
        
        pre {{
            background-color: #2d3748;
            color: #e2e8f0;
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1.5rem 0;
        }}
        
        pre code {{
            background: transparent;
            border: none;
            color: inherit;
        }}
        
        blockquote {{
            border-left: 4px solid {colors['primary']};
            padding-left: 1.5rem;
            margin: 1.5rem 0;
            font-style: italic;
            color: #64748b;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 1.5rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        footer {{
            text-align: center;
            padding: 2rem 0;
            color: #64748b;
            border-top: 1px solid #e2e8f0;
            margin-top: 3rem;
        }}
        
        @media (max-width: 768px) {{
            header h1 {{
                font-size: 2rem;
            }}
            main {{
                padding: 1.5rem;
                margin: 1rem auto;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{title}</h1>
            <p class="meta">Generated on {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
    </header>
    
    <main class="container">
        {content}
    </main>
    
    <footer class="container">
        <p>Created with File to Markdown Converter</p>
    </footer>
    
    <script>hljs.highlightAll();</script>
</body>
</html>'''
    
    def _minimal_template(self, content: str, title: str, colors: Dict[str, str], font: str = None) -> str:
        """Clean minimal template."""
        font_family = font or 'Georgia, serif'
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: {font_family};
            line-height: 1.8;
            color: #1a1a1a;
            background: #ffffff;
            max-width: 700px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }}
        
        h2, h3, h4, h5, h6 {{
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        
        p {{
            margin-bottom: 1rem;
        }}
        
        a {{
            color: #000;
            text-decoration: underline;
        }}
        
        code {{
            background-color: #f5f5f5;
            padding: 0.2em 0.4em;
            border-radius: 2px;
            font-family: 'Courier New', monospace;
        }}
        
        pre {{
            background-color: #f5f5f5;
            padding: 1rem;
            overflow-x: auto;
            margin: 1rem 0;
            border-left: 3px solid #000;
        }}
        
        blockquote {{
            border-left: 3px solid #000;
            padding-left: 1rem;
            margin: 1rem 0;
            font-style: italic;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        
        th, td {{
            padding: 0.5rem;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            font-weight: 600;
            border-bottom: 2px solid #000;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            margin: 1rem 0;
        }}
        
        .meta {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }}
        
        footer {{
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <article>
        <header>
            <h1>{title}</h1>
            <p class="meta">{datetime.now().strftime('%B %d, %Y')}</p>
        </header>
        
        {content}
        
        <footer>
            <p>Created with File to Markdown Converter</p>
        </footer>
    </article>
</body>
</html>'''
    
    def _classic_template(self, content: str, title: str, colors: Dict[str, str], font: str = None) -> str:
        """Classic document template."""
        font_family = font or '"Times New Roman", Times, serif'
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: {font_family};
            line-height: 1.6;
            color: #2c3e50;
            background: #f9f9f9;
            margin: 0;
            padding: 2rem;
        }}
        
        .document {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 3rem;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            text-align: center;
            font-size: 2rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .date {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 2rem;
            font-style: italic;
        }}
        
        h2, h3, h4 {{
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        
        p {{
            text-align: justify;
            margin-bottom: 1rem;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }}
        
        th, td {{
            padding: 0.75rem;
            border: 1px solid #bdc3c7;
        }}
        
        th {{
            background-color: #ecf0f1;
            font-weight: 600;
        }}
        
        code {{
            background-color: #ecf0f1;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        
        pre {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 1rem;
            overflow-x: auto;
            margin: 1rem 0;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 1rem;
            margin: 1rem 0;
            font-style: italic;
            color: #7f8c8d;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 1.5rem auto;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 2rem 0;
        }}
    </style>
</head>
<body>
    <div class="document">
        <h1>{title}</h1>
        <p class="date">{datetime.now().strftime('%B %d, %Y')}</p>
        
        {content}
    </div>
</body>
</html>'''
    
    def _dark_template(self, content: str, title: str, colors: Dict[str, str], font: str = None) -> str:
        """Dark theme template."""
        font_family = font or '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: {font_family};
            line-height: 1.6;
            color: #e2e8f0;
            background: #0f172a;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 3rem 0;
            border-bottom: 2px solid #475569;
        }}
        
        header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .meta {{
            opacity: 0.7;
            font-size: 0.95rem;
        }}
        
        main {{
            background: #1e293b;
            margin: 2rem auto;
            padding: 3rem;
            border-radius: 12px;
            border: 1px solid #334155;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: #38bdf8;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        
        h1 {{
            font-size: 2.5rem;
            border-bottom: 2px solid #38bdf8;
            padding-bottom: 0.5rem;
        }}
        
        h2 {{
            font-size: 2rem;
            border-bottom: 1px solid #475569;
            padding-bottom: 0.3rem;
        }}
        
        p {{
            margin-bottom: 1rem;
        }}
        
        a {{
            color: #38bdf8;
            text-decoration: none;
        }}
        
        a:hover {{
            color: #7dd3fc;
            text-decoration: underline;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }}
        
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #334155;
        }}
        
        th {{
            background-color: #334155;
            color: #38bdf8;
            font-weight: 600;
        }}
        
        tr:hover {{
            background-color: #334155;
        }}
        
        code {{
            background-color: #334155;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-size: 85%;
            color: #7dd3fc;
        }}
        
        pre {{
            background-color: #0f172a;
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1.5rem 0;
            border: 1px solid #334155;
        }}
        
        pre code {{
            background: transparent;
            color: inherit;
        }}
        
        blockquote {{
            border-left: 4px solid #38bdf8;
            padding-left: 1.5rem;
            margin: 1.5rem 0;
            color: #94a3b8;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 1.5rem 0;
        }}
        
        footer {{
            text-align: center;
            padding: 2rem 0;
            color: #64748b;
            border-top: 1px solid #334155;
            margin-top: 3rem;
        }}
        
        @media (max-width: 768px) {{
            header h1 {{
                font-size: 2rem;
            }}
            main {{
                padding: 1.5rem;
                margin: 1rem auto;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{title}</h1>
            <p class="meta">Generated on {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
    </header>
    
    <main class="container">
        {content}
    </main>
    
    <footer class="container">
        <p>Created with File to Markdown Converter</p>
    </footer>
    
    <script>hljs.highlightAll();</script>
</body>
</html>'''
    
    def get_available_templates(self):
        """Get list of available template names."""
        return list(self.templates.keys())
    
    def get_available_color_schemes(self):
        """Get list of available color schemes."""
        return list(self.color_schemes.keys())
