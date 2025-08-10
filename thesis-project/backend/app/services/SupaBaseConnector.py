from supabase import create_client, Client


class SupaBaseConnector:
    def __init__(self):
        self.url = "https://gsdvdncrnkbzyxgorxhy.supabase.co" 
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdzZHZkbmNybmtienl4Z29yeGh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM0OTQzMzEsImV4cCI6MjA1OTA3MDMzMX0.flxa9kDPshnG_vqVA3-XkLvsRfsdefv0EeKQM1ic5Q8"  # Replace with your Supabase API key
        self.supabase: Client = create_client(self.url, self.key)


    def select_initial_data(self):
        response = self.supabase.table("initial_data").select("*").execute()
        return response.data

    def select_questions(self):
        response = self.supabase.table("questions").select("*").execute()
        return response.data
    
    def select_neighbors(self):
        response = self.supabase.table("neighbors").select("*").execute()
        return response.data

    def fetch_data(self):
        return self.select_initial_data()
    
    def supabase_insert(self, table_name, data):
        response = self.supabase.table(table_name).insert(data).execute()
        return response.data[0]

    def wipe_data_of_table(self, table_name):
        response = self.supabase.table(table_name).delete().gte('id', 0).execute()
        print(response)

    def select_latest_results(self):
        response = self.supabase.table("results").select("*").order("id", desc=True).limit(1).execute()
        return response.data




