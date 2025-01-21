from supabase_manager import get_supabase_client
import bcrypt

class UserModel:
    def __init__(self):
        self.client = get_supabase_client()

    def check_student_record(self, student_id, last_name):
        try:
            response = (
                self.client.table("student_records")
                .select("*")
                .eq("student_id", student_id)
                .eq("last_name", last_name)
                .execute()
            )
            return response.data
        except Exception as e:
            return {"error": str(e)}

    def check_teacher_record(self, last_name, teacher_id):
        try:
            response = (
                self.client.table("teacher_records")
                .select("*")
                .eq("teacher_id", teacher_id)
                .eq("last_name", last_name)
                .execute()
            )
            return response.data
        except Exception as e:
            return {"error": str(e)}

    def check_user_id(self, user_id):
        try:
            teacher_response = self.client.table("teacher_table").select("*").eq("teacher_id", user_id).execute()
            student_response = self.client.table("student_table").select("*").eq("student_id", user_id).execute()

            if teacher_response.data:
                return {"status": "found", "role": "teacher", "data": teacher_response.data}
            elif student_response.data:
                return {"status": "found", "role": "student", "data": student_response.data}
            else:
                return {"status": "not_found", "message": "ID not found in records."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def check_email(self, email):
        try:
            teacher_response = self.client.table("teacher_table").select("*").eq("email", email).execute()
            student_response = self.client.table("student_table").select("*").eq("email", email).execute()

            if teacher_response.data:
                return {"status": "found", "role": "teacher", "data": teacher_response.data}
            elif student_response.data:
                return {"status": "found", "role": "student", "data": student_response.data}
            else:
                return {"status": "not_found", "message": "Email not found in records."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def login_checker(self, email, password):
        try:
            for role, table in [("teacher", "teacher_table"), ("student", "student_table")]:
                response = self.client.table(table).select("*").eq("email", email).execute()
                if response.data:
                    user = response.data[0]
                    if self.verify_password(password, user.get("password")):
                        full_name = f"{user.get('first_name')} {user.get('last_name')}"

                        # Check the role and fetch either student_id or teacher_id
                        if role == "teacher":
                            teacher_id = user.get("teacher_id", None)
                            return {
                                "status": "found",
                                "role": role,
                                "teacher_id": teacher_id,  # Return teacher_id for teachers
                                "full_name": full_name,
                                "message": f"Welcome, {user.get('last_name')}",
                                "data": user,
                            }
                        else:
                            student_id = user.get("student_id", None)
                            return {
                                "status": "found",
                                "role": role,
                                "student_id": student_id,  # Return student_id for students
                                "full_name": full_name,
                                "message": f"Welcome, {user.get('last_name')}",
                                "data": user,
                            }
                    return {"status": "not_found", "message": "Incorrect email or password."}
            return {"status": "not_found", "message": "Incorrect email or password."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def insert_student(self, data):
        try:
            response = self.client.table("student_table").insert(data).execute()
            return response
        except Exception as e:
            return {"error": str(e)}

    def insert_teacher(self, data):
        try:
            response = self.client.table("teacher_table").insert(data).execute()
            return response
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))