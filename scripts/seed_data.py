#!/usr/bin/env python3
"""
Seed data script for Crafty CRM database using Faker.

This script populates the database with realistic sample data for development and testing.
Run this script after the database is initialized.
"""

import json
from datetime import datetime, timedelta
import random
from faker import Faker
from connectors.database import Database


class DatabaseSeeder:
    def __init__(self):
        self.db = Database()
        self.fake = Faker()
        # Set seed for reproducible results
        Faker.seed(12345)

    def seed_companies(self, count=50):
        """Seed companies table with realistic company data."""
        print(f"Seeding {count} companies...")

        # Generate all company data at once
        companies_data = []
        for _ in range(count):
            companies_data.append({"Company_name": self.fake.company()})

        # Batch insert
        query = """
            INSERT INTO companies (Company_name)
            VALUES (%(Company_name)s)
            ON CONFLICT DO NOTHING
        """

        self._batch_insert(query, companies_data)
        print(f"Completed seeding {count} companies")

    def seed_contacts(self, count=200):
        """Seed contacts table with realistic contact data."""
        print(f"Seeding {count} contacts...")

        # Get company IDs for foreign key relationships
        companies_df = self.db.execute_query_df("SELECT Company_id FROM companies")
        if companies_df.empty:
            print("No companies found. Please seed companies first.")
            return

        # Find the correct column name
        company_id_col = self._find_column(
            companies_df, ["Company_id", "company_id", "companyid"]
        )
        if company_id_col is None:
            raise ValueError("Could not find Company_id column")

        company_ids = companies_df[company_id_col].tolist()

        # Generate all contact data at once
        contacts_data = []
        for _ in range(count):
            contacts_data.append(
                {
                    "Contact_name": self.fake.name(),
                    "Email": self.fake.email(),
                    "Company_id": random.choice(company_ids),
                }
            )

        # Batch insert
        query = """
            INSERT INTO contacts (Contact_name, Email, Company_id)
            VALUES (%(Contact_name)s, %(Email)s, %(Company_id)s)
            ON CONFLICT DO NOTHING
        """

        self._batch_insert(query, contacts_data)
        print(f"Completed seeding {count} contacts")

    def seed_client_engagements(self, count=500):
        """Seed client_engagements table with realistic engagement data."""
        print(f"Seeding {count} client engagements...")

        # Get contact and company IDs
        contacts_df = self.db.execute_query_df(
            "SELECT Contact_id, Company_id FROM contacts"
        )
        if contacts_df.empty:
            print("No contacts found. Please seed contacts first.")
            return

        # Find the correct column names
        contact_id_col = self._find_column(
            contacts_df, ["Contact_id", "contact_id", "contactid"]
        )
        company_id_col = self._find_column(
            contacts_df, ["Company_id", "company_id", "companyid"]
        )

        if contact_id_col is None or company_id_col is None:
            raise ValueError("Could not find required columns")

        engagement_types = [
            "Phone Call",
            "Email",
            "Meeting",
            "Demo",
            "Follow-up",
            "Proposal",
            "Contract Review",
            "Training",
            "Support Call",
        ]

        # Generate all engagement data at once
        engagements_data = []
        for _ in range(count):
            # Randomly select a contact and use their company
            contact_row = contacts_df.sample(n=1).iloc[0]

            # Generate a random timestamp within the last 6 months
            days_ago = random.randint(0, 180)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            timestamp = datetime.now() - timedelta(
                days=days_ago, hours=hours_ago, minutes=minutes_ago
            )

            engagements_data.append(
                {
                    "Timestamp": timestamp,
                    "Type": random.choice(engagement_types),
                    "Contact_id": contact_row[contact_id_col],
                    "Company_id": contact_row[company_id_col],
                }
            )

        # Batch insert
        query = """
            INSERT INTO client_engagements (Timestamp, Type, Contact_id, Company_id)
            VALUES (%(Timestamp)s, %(Type)s, %(Contact_id)s, %(Company_id)s)
            ON CONFLICT DO NOTHING
        """

        self._batch_insert(query, engagements_data)
        print(f"Completed seeding {count} client engagements")

    def seed_support_tickets(self, count=300):
        """Seed support_tickets table with realistic ticket data."""
        print(f"Seeding {count} support tickets...")

        # Get contact and company IDs
        contacts_df = self.db.execute_query_df(
            "SELECT Contact_id, Company_id FROM contacts"
        )
        if contacts_df.empty:
            print("No contacts found. Please seed contacts first.")
            return

        # Find the correct column names
        contact_id_col = self._find_column(
            contacts_df, ["Contact_id", "contact_id", "contactid"]
        )
        company_id_col = self._find_column(
            contacts_df, ["Company_id", "company_id", "companyid"]
        )

        if contact_id_col is None or company_id_col is None:
            raise ValueError("Could not find required columns")

        ticket_subjects = [
            "Login issues with the platform",
            "Payment processing error",
            "Feature request for mobile app",
            "Bug report: data not syncing",
            "Account access problems",
            "Integration setup assistance",
            "Performance optimization request",
            "Security concern about data",
            "UI/UX improvement suggestion",
            "API documentation needed",
            "Billing inquiry",
            "Training session request",
            "Custom report generation",
            "Data export functionality",
            "Mobile app crash report",
        ]

        statuses = ["Open", "In Progress", "Resolved", "Closed", "Pending"]

        # Generate all ticket data at once
        tickets_data = []
        for _ in range(count):
            # Randomly select a contact and use their company
            contact_row = contacts_df.sample(n=1).iloc[0]

            # Generate random timestamps
            days_ago = random.randint(0, 90)
            created_at = datetime.now() - timedelta(days=days_ago)

            # 70% of tickets are closed
            status = random.choice(statuses)
            closed_at = None
            if status in ["Resolved", "Closed"] and random.random() < 0.7:
                closed_at = created_at + timedelta(days=random.randint(1, 30))

            # Generate realistic properties JSON
            properties = {
                "priority": random.choice(["Low", "Medium", "High", "Critical"]),
                "category": random.choice(
                    ["Technical", "Billing", "Feature Request", "Bug Report", "General"]
                ),
                "assigned_to": self.fake.name() if random.random() < 0.8 else None,
                "tags": random.sample(
                    ["urgent", "customer", "vip", "escalated"], random.randint(0, 2)
                ),
                "source": random.choice(["Email", "Phone", "Web Form", "Chat", "API"]),
                "response_time_hours": random.randint(1, 48),
            }

            tickets_data.append(
                {
                    "Created_at": created_at,
                    "Closed_at": closed_at,
                    "Status": status,
                    "Subject": random.choice(ticket_subjects),
                    "Company_id": contact_row[company_id_col],
                    "Contact_id": contact_row[contact_id_col],
                    "Properties": json.dumps(properties),
                }
            )

        # Batch insert
        query = """
            INSERT INTO support_tickets (Created_at, Closed_at, Status, Subject, Company_id, Contact_id, Properties)
            VALUES (%(Created_at)s, %(Closed_at)s, %(Status)s, %(Subject)s, %(Company_id)s, %(Contact_id)s, %(Properties)s)
            ON CONFLICT DO NOTHING
        """

        self._batch_insert(query, tickets_data)
        print(f"Completed seeding {count} support tickets")

    def _find_column(self, df, possible_names):
        """Helper method to find the correct column name."""
        for col in possible_names:
            if col in df.columns:
                return col
        return None

    def _batch_insert(self, query, data_list, batch_size=1000):
        """Execute batch inserts for better performance."""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cursor:
                for i in range(0, len(data_list), batch_size):
                    batch = data_list[i : i + batch_size]
                    cursor.executemany(query, batch)
                    conn.commit()

                    # Progress indicator for large batches
                    if len(data_list) > batch_size:
                        progress = min(i + batch_size, len(data_list))
                        print(f"  Processed {progress}/{len(data_list)} records...")
        except Exception as e:
            print(f"Batch insert failed: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def run_all(
        self,
        companies_count=50,
        contacts_count=200,
        engagements_count=500,
        tickets_count=300,
    ):
        """Run all seed functions with specified counts."""
        print("Starting database seeding with Faker...")

        try:
            # Test connection first
            if not self.db.test_connection():
                print("Failed to connect to database. Please check your configuration.")
                return

            print("Seeding companies...")
            self.seed_companies(companies_count)

            print("Seeding contacts...")
            self.seed_contacts(contacts_count)

            print("Seeding client engagements...")
            self.seed_client_engagements(engagements_count)

            print("Seeding support tickets...")
            self.seed_support_tickets(tickets_count)

            print("Database seeding completed successfully!")

            # Print summary
            self.print_summary()

        except Exception as e:
            print(f"Error during seeding: {e}")
        finally:
            self.db.close_connection()

    def print_summary(self):
        """Print a summary of the seeded data."""
        try:
            companies_count = self.db.execute_query_df(
                "SELECT COUNT(*) as count FROM companies"
            ).iloc[0]["count"]
            contacts_count = self.db.execute_query_df(
                "SELECT COUNT(*) as count FROM contacts"
            ).iloc[0]["count"]
            engagements_count = self.db.execute_query_df(
                "SELECT COUNT(*) as count FROM client_engagements"
            ).iloc[0]["count"]
            tickets_count = self.db.execute_query_df(
                "SELECT COUNT(*) as count FROM support_tickets"
            ).iloc[0]["count"]

            print("\n" + "=" * 50)
            print("SEEDING SUMMARY")
            print("=" * 50)
            print(f"Companies: {companies_count}")
            print(f"Contacts: {contacts_count}")
            print(f"Client Engagements: {engagements_count}")
            print(f"Support Tickets: {tickets_count}")
            print("=" * 50)

        except Exception as e:
            print(f"Error getting summary: {e}")


def main():
    """Main function to run the seeder."""
    import argparse

    parser = argparse.ArgumentParser(description="Seed the database with sample data")
    parser.add_argument(
        "--companies", type=int, default=50, help="Number of companies to seed"
    )
    parser.add_argument(
        "--contacts", type=int, default=200, help="Number of contacts to seed"
    )
    parser.add_argument(
        "--engagements", type=int, default=500, help="Number of engagements to seed"
    )
    parser.add_argument(
        "--tickets", type=int, default=300, help="Number of tickets to seed"
    )

    args = parser.parse_args()

    seeder = DatabaseSeeder()
    seeder.run_all(
        companies_count=args.companies,
        contacts_count=args.contacts,
        engagements_count=args.engagements,
        tickets_count=args.tickets,
    )


if __name__ == "__main__":
    main()
