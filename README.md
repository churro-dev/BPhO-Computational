# Streamlit Base

## Intended Use

### Gist

This is a *template repository*, so its intended use is to create other repositories which **build off of this web app template**.

### Use cases

Set up by default with an **authentication system** - this is suited for general websites, but of course also works for data display apps.


## Dependencies

All requirements are listed in ***requirements.txt***


## Authentication

### Authentication Widgets

Uses streamlit-authenticator library for authentication widgets

### Credentials

Credentials are stored in ***config.yaml***


## Config && Secrets

### Config

Configuration for Streamlit is stored in ***/.streamlit/config.toml***

### Secrets

Secrets for Streamlit environment are stored in ***/.streamlit/secrets.toml***


## Github Actions

### Pylint

Default Pylint Github Action is set up in ***/.github/workflows/pylint.yml***
