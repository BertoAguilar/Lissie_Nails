from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Appointment:
    db = "lissie_nails_v1"

    def __init__(self, data):
        self.id = data["id"]
        self.appointment_date_time = data["appointment_date_time"]
        self.comments = data["comments"]
        self.appointment_type = data["appointment_type"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None

    @classmethod
    def get_appointments(cls):
        """This Method Selects All Appointments"""
        query = """
        SELECT * FROM appointments
        JOIN users
        ON appointments.users_id = users.id
        ORDER BY appointment_date_time ASC;
        """
        results = connectToMySQL(Appointment.db).query_db(query)
        appointments = []
        for each_result in results:
            appointment = Appointment(each_result)
            user_data = {
                "id": each_result["users.id"],
                "first_name": each_result["first_name"],
                "last_name": each_result["last_name"],
                "email": each_result["email"],
                "password": each_result["password"],
                "created_at": each_result["users.created_at"],
                "updated_at": each_result["users.updated_at"],
            }
            user = User(user_data)
            appointment.user = user
            appointments.append(appointment)
        return appointments

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO appointments 
        (users_id, appointment_date_time, appointment_type, comments)
        VALUES (%(users_id)s,
        %(appointment_date_time)s,
        %(appointment_type)s,
        %(comments)s);"""
        print(query)
        return connectToMySQL(Appointment.db).query_db(query, data)

    def validate_appointment(appointment):
        is_valid = True
        if len(appointment["appointment_date_time"]) == 0:
            flash("Appointment Date must be selected.")
            is_valid = False
        if len(appointment["appointment_type"]) == 0:
            flash("Appointment Type is Empty!")
            is_valid = False
        if len(appointment["comments"]) < 3:
            flash("Comments must be at least 3 characters.")
            is_valid = False
        #     print("****************************************")
        #     print(appointment["under_thirty"])
        # if len(appointment["under_thirty"]) == 0:
        #     flash("Is it under 30 min is Empty!")
        #     is_valid = False
        return is_valid

    @classmethod
    def destroy_appointment(cls, appointment_id):
        query = "DELETE FROM appointments WHERE id = %(appointment_id)s;"
        data = {"appointment_id": appointment_id}
        print("***********************************************")
        print(query)
        connectToMySQL(Appointment.db).query_db(query, data)
        return

    @classmethod
    def get_one_appointment(cls, appointment_id):
        query = "SELECT * FROM appointments WHERE id= %(appointment_id)s;"
        data = {"appointment_id": appointment_id}
        list_of_dicts = connectToMySQL(Appointment.db).query_db(query, data)
        appointments = Appointment(list_of_dicts[0])
        return appointments

    @classmethod
    def get_one_appointment(cls, appointment_id):
        query = "SELECT * FROM appointments WHERE id= %(appointment_id)s;"
        data = {"appointment_id": appointment_id}
        list_of_dicts = connectToMySQL(Appointment.db).query_db(query, data)
        appointments = Appointment(list_of_dicts[0])
        return appointments

    # ==================================TEST TEST TEST===============================
    @classmethod
    def get_one_appointment_detailed(cls, appointment_id):
        """This Method Selects All Appointments"""
        query = """
        SELECT * FROM appointments
        JOIN users
        ON appointments.users_id = users.id
        WHERE appointments.id = %(appointment_id)s;
        """
        data = {"appointment_id": appointment_id}
        results = connectToMySQL(Appointment.db).query_db(query, data)
        appointment = Appointment(results[0])
        each_result = results[0]
        user_data = {
            "id": each_result["users.id"],
            "first_name": each_result["first_name"],
            "last_name": each_result["last_name"],
            "email": each_result["email"],
            "password": each_result["password"],
            "created_at": each_result["users.created_at"],
            "updated_at": each_result["users.updated_at"],
        }
        user = User(user_data)
        appointment.user = user
        return appointment

    # ==================================TEST TEST TEST===============================

    @classmethod
    def update_appointment(cls, data):
        query = """
        UPDATE appointments SET 
        appointment_date_time = %(appointment_date_time)s, 
        appointment_type = %(appointment_type)s, 
        comments = %(comments)s
        WHERE id= %(appointment_id)s;"""
        return connectToMySQL(Appointment.db).query_db(query, data)
