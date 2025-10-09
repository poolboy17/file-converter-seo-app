#!/usr/bin/env python3
"""
Push the entire project to a new GitHub repository
"""
import base64
import json
import os
from pathlib import Path

import requests


def get_github_token():
    """Get GitHub access token from Replit connection"""
    hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
    x_replit_token = None
    
    if os.environ.get('REPL_IDENTITY'):
        x_replit_token = 'repl ' + os.environ.get('REPL_IDENTITY')
    elif os.environ.get('WEB_REPL_RENEWAL'):
        x_replit_token = 'depl ' + os.environ.get('WEB_REPL_RENEWAL')
    
    if not x_replit_token:
        raise Exception('Authentication token not found')
    
    url = f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=github'
    headers = {
        'Accept': 'application/json',
        'X_REPLIT_TOKEN': x_replit_token
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if not data.get('items') or len(data['items']) == 0:
        raise Exception('GitHub not connected')
    
    connection_settings = data['items'][0]
    access_token = connection_settings.get('settings', {}).get('access_token')
    
    if not access_token:
        oauth_creds = connection_settings.get('settings', {}).get('oauth', {}).get('credentials', {})
        access_token = oauth_creds.get('access_token')
    
    if not access_token:
        raise Exception('Access token not found')
    
    return access_token

def get_github_user(token):
    """Get authenticated GitHub user info"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get('https://api.github.com/user', headers=headers)
    return response.json()

def create_repository(token, repo_name, description, private=False):
    """Create a new GitHub repository"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': repo_name,
        'description': description,
        'private': private,
        'auto_init': False
    }
    
    response = requests.post('https://api.github.com/user/repos', headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to create repository: {response.status_code} - {response.text}")

def get_project_files():
    """Get all project files to push"""
    files_to_push = []
    
    # Define directories and files to include
    include_patterns = [
        'app.py',
        'replit.md',
        'pyproject.toml',
        'uv.lock',
        'converters/**/*.py',
        'utils/**/*.py',
        'templates/**/*',
        '.streamlit/**/*'
    ]
    
    # Files/directories to exclude
    exclude_patterns = [
        '__pycache__',
        '*.pyc',
        '.git',
        'venv',
        'env',
        '.env',
        'node_modules',
        '.replit',
        'replit.nix',
        '.config',
        '.cache',
        '.upm'
    ]
    
    base_path = Path('.')
    
    # Walk through directory
    for item in base_path.rglob('*'):
        if item.is_file():
            # Check if should exclude
            should_exclude = False
            for exclude in exclude_patterns:
                if exclude in str(item):
                    should_exclude = True
                    break
            
            if not should_exclude:
                try:
                    relative_path = item.relative_to(base_path)
                    files_to_push.append(str(relative_path))
                except:
                    pass
    
    return files_to_push

def push_files_to_github(token, owner, repo_name, files):
    """Push files to GitHub using the API"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    base_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents'
    
    pushed_count = 0
    failed_files = []
    
    for file_path in files:
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Encode to base64
            encoded_content = base64.b64encode(content).decode('utf-8')
            
            # Create/update file
            data = {
                'message': f'Add {file_path}',
                'content': encoded_content
            }
            
            url = f'{base_url}/{file_path}'
            response = requests.put(url, headers=headers, json=data)
            
            if response.status_code in [200, 201]:
                pushed_count += 1
                print(f"✓ Pushed: {file_path}")
            else:
                failed_files.append(file_path)
                print(f"✗ Failed: {file_path} ({response.status_code})")
        except Exception as e:
            failed_files.append(file_path)
            print(f"✗ Error pushing {file_path}: {str(e)}")
    
    return pushed_count, failed_files

def main():
    import sys
    
    print("=== Pushing Project to GitHub ===\n")
    
    # Get GitHub token
    print("1. Getting GitHub access token...")
    try:
        token = get_github_token()
        print("   ✓ Token retrieved\n")
    except Exception as e:
        print(f"   ✗ Failed to get token: {e}")
        return
    
    # Get user info
    print("2. Getting GitHub user info...")
    try:
        user = get_github_user(token)
        username = user['login']
        print(f"   ✓ Authenticated as: {username}\n")
    except Exception as e:
        print(f"   ✗ Failed to get user info: {e}")
        return
    
    # Repository details
    if len(sys.argv) > 1:
        repo_name = sys.argv[1]
    else:
        repo_name = "file-converter-app"
    
    description = "Multi-format file converter with SEO optimization - converts DOCX, CSV, TXT, WXR to Markdown and HTML"
    
    if len(sys.argv) > 2 and sys.argv[2].lower() == 'private':
        private = True
    else:
        private = False
    
    # Create repository
    print(f"\n3. Creating repository '{repo_name}'...")
    try:
        repo = create_repository(token, repo_name, description, private)
        repo_url = repo['html_url']
        print(f"   ✓ Repository created: {repo_url}\n")
    except Exception as e:
        print(f"   ✗ Failed to create repository: {e}")
        return
    
    # Get files to push
    print("4. Scanning project files...")
    files = get_project_files()
    print(f"   ✓ Found {len(files)} files to push\n")
    
    # Push files
    print("5. Pushing files to GitHub...")
    pushed_count, failed_files = push_files_to_github(token, username, repo_name, files)
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Repository: {repo_url}")
    print(f"Files pushed: {pushed_count}/{len(files)}")
    
    if failed_files:
        print(f"\nFailed files ({len(failed_files)}):")
        for file in failed_files:
            print(f"  - {file}")
    else:
        print("\n✓ All files pushed successfully!")
    
    print(f"\nYou can view your repository at: {repo_url}")

if __name__ == "__main__":
    main()
