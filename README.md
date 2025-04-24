# Inventory Collector

A simple tool for collecting basic hardware and software inventory from network devices via CLI and SNMP.

## Features
- Platform autodetection (SNMP-based)
- TTP-powered template parsing
- Unified inventory model
- Pluggable collectors per vendor
- CLI interface for direct calls

## Configuration

Secrets are loaded from a `.env` file.  
Use the provided `.env.example` as a starting point and create your own:

```bash
cp .env.example .env


## Usage

```bash
python main.py --ip 192.168.1.10
