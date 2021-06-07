from neo4j import GraphDatabase
import datetime
import sys

import services.config as config

class Neo4jConnection:
    @staticmethod
    def _initDB(tx):
        tx.run("MERGE (online:Status {name: \"Online\"})")
        tx.run("MERGE (offline:Status {name: \"Offline\"})")
        tx.run("MERGE (:Tag {name: \"General\"})")
        tx.run("MERGE (:Tag {name: \"Important\"})")
        tx.run("MERGE (:Tag {name: \"Ad\"})")
        tx.run("MERGE (:Tag {name: \"Social\"})")
        tx.run("MERGE (:Tag {name: \"Info\"})")
        tx.run("MERGE (:Status {name: \"Created\"})")
        tx.run("MERGE (:Status {name: \"In the queue\"})")
        tx.run("MERGE (:Status {name: \"Spam check\"})")
        tx.run("MERGE (:Status {name: \"Blocked\"})")
        tx.run("MERGE (:Status {name: \"Sent\"})")
        tx.run("MERGE (:Status {name: \"Delivered\"})")
        tx.run("MERGE (:Worker)")

    def initDB(self):
        with self.driver.session(database="neo4j") as session:
            session.write_transaction(self._initDB)

    def __init__(self):
        self.driver = GraphDatabase.driver(config.Neo4j.HOST.value, auth=(config.Neo4j.USER.value, config.Neo4j.PWD.value))
        self.initDB()

    def close(self):
        self.driver.close()

    def user_online(self, username):
        with self.driver.session(database="neo4j") as session:
            session.write_transaction(self._user_online, username)

    @staticmethod
    def _user_online(tx, username):
        tx.run("MERGE (a:User {username: $username})", username=username)
        tx.run("MATCH (a:User {username: $username})-[r:IS]->(:Status)"
                "DELETE (r)", username=username)
        tx.run("MATCH (a:User {username: $username}), (online:Status {name: \"Online\"})"
                "CREATE (a)-[:IS]->(online)", username=username)

    def user_offline(self, user):
        with self.driver.session(database="neo4j") as session:
            session.write_transaction(self._user_offline, user)

    @staticmethod
    def _user_offline(tx, username):
        tx.run("MERGE (a:User {username: $username})", username=username)
        tx.run("MATCH (a:User {username: $username})-[r:IS]->(:Status)"
                "DELETE (r)", username=username)
        tx.run("MATCH (a:User {username: $username}), (offline:Status {name: \"Offline\"})"
                "CREATE (a)-[:IS]->(offline)", username=username)

    def send_message(self, sender, receiver, message, tag, id):
        with self.driver.session(database="neo4j") as session:
            session.write_transaction(self._send_message, sender, receiver, message, tag, id)

    @staticmethod
    def _send_message(tx, sender, receiver, content, tag, id):
        tx.run("MERGE (a:User {username: $receiver})", receiver=receiver)
        tx.run("CREATE (message:Message {content: $content, time: $time, id: $id})",
                content=content, time=datetime.datetime.now(), id=id)
        tx.run("MATCH (sender:User {username: $sender}), (receiver:User {username: $receiver}), (message:Message {id: $id})"
                "CREATE (sender)-[:SENDS]->(message), (message)-[:DIRECTED]->(receiver)",
                sender=sender, receiver=receiver, id=id)
        tx.run("MATCH (message:Message {id: $id}), (tag:Tag {name: $tag})"
                "CREATE (message)-[:BELONGS]->(tag)",
                id=id, tag=tag)
        tx.run("MATCH (message: Message {id: $id}), (tag:Status {name: $status})"
                "CREATE (message)-[:IN]->(tag)",
                id=id, status=config.MessageState.CREATED)

    def set_message_status(self, message_id, status):
        with self.driver.session(database="neo4j") as session:
            session.write_transaction(self._set_message_status, message_id, status)

    @staticmethod
    def _set_message_status(tx, message_id, status):
        if status == config.MessageState.BLOCKED:
            tx.run("MATCH (message:Message {id: $id}), (worker:Worker)"
                "CREATE (worker)-[:BLOCKS]->(message)",
                id=message_id)
        tx.run("MATCH (message:Message {id:$id})-[r:IN]->(:Status)"
                "DELETE r",
                id=message_id)
        tx.run("MATCH (message:Message {id:$id}), (status:Status {name: $status})"
                "CREATE (message)-[:IN]->(status)",
                id=message_id, status=status)
        

connection = Neo4jConnection()