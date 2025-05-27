# app/models/appointment.py

# 简易挂号记录存储（内存版）
appointments = []

def create_appointment(department, doctor, time):
    appointment = {
        'department': department,
        'doctor': doctor,
        'time': time
    }
    appointments.append(appointment)
    # 这里你可以改成写入数据库或文件
    print(f"新挂号：{appointment}")
    return True

def list_appointments():
    return appointments
