#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@example.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = \$PORT\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
\n\
[theme]\n\
primaryColor = \"#FF4B4B\"\n\
backgroundColor = \"#0E1117\"\n\
secondaryBackgroundColor = \"#262730\"\n\
textColor = \"#FAFAFA\"\n\
font = \"sans serif\"\n\
" > ~/.streamlit/config.toml
