import requests
import json
import os

# GitHub Personal Access Token (needed for authenticated API requests)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"
ORG_NAME = "gitlab-migration"  # Replace with your organization name

# Headers for authenticated GitHub API requests
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Function to list all repositories in the organization
def list_org_repos():
    repos = []
    url = f"{GITHUB_API_URL}/orgs/{ORG_NAME}/repos"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repos = [repo['full_name'] for repo in response.json()]
    else:
        print(f"Error fetching repos: {response.status_code}")
    return repos

# Function to get the languages used in a repository
def get_languages(repo):
    url = f"{GITHUB_API_URL}/repos/{repo}/languages"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

# Function to get dependencies from common files (including Go specific files)
def get_dependencies(repo):
    dependencies = []
    common_files = ["package.json", "requirements.txt", "Pipfile", "pom.xml", "go.mod", "go.sum"]
    for file in common_files:
        url = f"{GITHUB_API_URL}/repos/{repo}/contents/{file}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            dependencies.append(file)
    return dependencies

# Main function to extract technology data
def extract_tech_data():
    tech_data = []
    repos = list_org_repos()
    for repo in repos:
        languages = get_languages(repo)
        dependencies = get_dependencies(repo)
        tech_data.append({
            "repo": repo,
            "languages": languages,
            "dependencies": dependencies
        })
    return tech_data

# Function to save data as a JSON file
def save_to_json(data, filename="tech_data.json"):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    data = extract_tech_data()
    save_to_json(data)
