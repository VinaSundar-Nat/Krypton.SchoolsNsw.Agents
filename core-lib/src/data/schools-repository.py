class SchoolsRepository:
    def __init__(self, db_driver):
        self.db_driver = db_driver

    def fetch_school(self, school_id):
        query = "MATCH (s:School {id: $id}) RETURN s"
        with self.db_driver.session() as session:
            result = session.run(query, id=school_id)
            records = [dict(r) for r in result]
            return str(records)

    def insert_school(self, school_data):
        query = "CREATE (s:School $data)"
        with self.db_driver.session() as session:
            result = session.run(query, data=school_data)
            return f"Inserted {result.summary().counters.nodes_created} nodes."
        
    def update_school(self, school_id, update_data):
        query = "MATCH (s:School {id: $id}) SET s += $data"
        with self.db_driver.session() as session:
            result = session.run(query, id=school_id, data=update_data)
            return f"Updated {result.summary().counters.properties_set} properties."