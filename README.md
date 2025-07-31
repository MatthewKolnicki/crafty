# Crafty

I've implemented API endpoints for both the Python and SQL questions.
In cases where the question was not clear to me, I've made assumptions or created multiple implementations.
These will be called out in comments throughout the code in /services and /routers.

I've added a docker-compose file to start a postgres database locally and a seeding script to populate the database with realistic data.

This API has been deployed to AWS Lambda using serverless framework and I can securely share the API url with you.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the database:**
   ```bash
   docker-compose up -d
   ```

3. **Run the API:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Seeding

Creates a larger dataset with realistic data:
```bash
python scripts/seed_data.py
```

You can customize the amount of data:
```bash
python scripts/seed_data.py --companies 100 --contacts 500 --engagements 1000 --tickets 600
```

## Database Schema

The seeding system works with the following tables:

- **companies**: Company information
- **contacts**: Contact persons with company relationships
- **client_engagements**: Interaction history with clients
- **support_tickets**: Support ticket system with JSON properties

## Features

- **Realistic Data**: Uses Faker library for realistic company names, emails, and contact information
- **Proper Relationships**: Maintains referential integrity between tables
- **JSON Properties**: Support tickets include structured JSON data for metadata

## Clean Up
I don't expect you would have any conflicting containers with crafty-postgres, but run at your own risk if you have other sensitive containers or volumes. This will delete the database container and all data. 
```bash
./scripts/cleanup.sh
```
